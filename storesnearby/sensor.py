"""Google Places sensor platform."""
from requests_futures.sessions import FuturesSession
from requests import (
    RequestException,
    ConnectionError,
    HTTPError,
    URLRequired,
    TooManyRedirects,
    ConnectTimeout,
    ReadTimeout,
    Timeout,
    JSONDecodeError,
)
# from collections.abc import Mapping

import logging
import voluptuous as vol
from typing import Any, Callable, Dict, Optional
from urllib import parse
from datetime import datetime, timedelta

from homeassistant.const import (
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    API_KEY,
    BASE_API_URL,
    ATTR_NAME,
    ATTR_COMMERCIAL_NAME,
    ATTR_PLACEID,
    ATTR_OPENING_HOURS_0,
    ATTR_OPENING_HOURS_1,
    ATTR_OPENING_HOURS_2,
    ATTR_OPENING_HOURS_3,
    ATTR_OPENING_HOURS_4,
    ATTR_OPENING_HOURS_5,
    ATTR_OPENING_HOURS_6,
    ATTR_LAST_FORCED_UPDATE,
    ATTR_OPEN_NOW,
    API_RESULT,
    API_NAME,
    API_WEEKDAY_TEXT,
    API_OPENING_HOURS,
    API_OPEN_NOW,
    CONF_STORES,
    CONF_NAME,
    CONF_PLACEID,
)

_LOGGER = logging.getLogger(__name__)

"""Time between updates from Google Places API."""
SCAN_INTERVAL = timedelta(weeks=2)

"""Schéma de configuration.yaml"""
STORES_SCHEMA = vol.Schema(
    {vol.Required(CONF_NAME): cv.string, vol.Required(CONF_PLACEID): cv.string}
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_STORES): vol.All(cv.ensure_list, [STORES_SCHEMA]),
    }
)

async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """ Set up the sensor platform """
    sensors = [StoreNearbySensor(store) for store in config[CONF_STORES]]
    _LOGGER.info(f"Added {len(sensors)} store(s) nearby")
    async_add_entities(sensors, update_before_add=True)

class StoreNearbySensor(Entity):
    """Representation of a Stores Nearby Sensor."""

    def __init__(self, store: Dict[str, str]):
        super().__init__()
        self._name = store[CONF_NAME]
        self.place_id = store[CONF_PLACEID]
        self.attrs: Dict[str, Any] = {ATTR_NAME: self._name, ATTR_PLACEID: self.place_id}
        self._state = None
        self._available = True;

    @property
    def name(self) -> str:
        """Return the visual name of the store as setup in the configuration.yaml."""
        return f"{self._name}"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f"storenearby-{self.place_id[:7]}"
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> Optional[str]:
        """Return the state of entity."""
        return self._state

    @property
    def state_attributes(self) -> Dict[str, Any] | None:
        """Return the attributes."""
        return self.attrs

    async def async_update(self):
        try:
            parameters = f"?key={API_KEY}&place_id={self.place_id}&fields=name%2Copening_hours"
            url = BASE_API_URL + parameters

            """Launch the query"""
            session = FuturesSession()
            future_response = session.get(url)

            """Wait for the answer."""
            response = future_response.result()

            """Convert the response in json."""
            resp_json = response.json()

            self.attrs[ATTR_COMMERCIAL_NAME] = resp_json.get(API_RESULT).get(API_NAME)
            self.attrs[ATTR_OPEN_NOW] = resp_json.get(API_RESULT).get(API_OPENING_HOURS).get(API_OPEN_NOW)

            """Ugly.. i cant find how to make this work : f"{ATTR_OPENING_HOURS_{i}}"""
            weekday_text = resp_json.get("result").get(API_OPENING_HOURS).get(API_WEEKDAY_TEXT)
            for i in range(0, len(weekday_text)):
                if i == 0:
                    self.attrs[ATTR_OPENING_HOURS_0] = weekday_text[i]
                elif i == 1:
                    self.attrs[ATTR_OPENING_HOURS_1] = weekday_text[i]
                elif i == 2:
                    self.attrs[ATTR_OPENING_HOURS_2] = weekday_text[i]
                elif i == 3:
                    self.attrs[ATTR_OPENING_HOURS_3] = weekday_text[i]
                elif i == 4:
                    self.attrs[ATTR_OPENING_HOURS_4] = weekday_text[i]
                elif i == 5:
                    self.attrs[ATTR_OPENING_HOURS_5] = weekday_text[i]
                elif i == 6:
                    self.attrs[ATTR_OPENING_HOURS_6] = weekday_text[i]

            mynow = datetime.now()
            nowstr = "%04d-%02d-%02dT%02d:%02d:%02d" % (mynow.year, mynow.month, mynow.day, mynow.hour, mynow.minute, mynow.second)
            self.attrs[ATTR_LAST_FORCED_UPDATE] = nowstr

            self._available = True
            self._state = 1

        except RequestException as e:
            self._available = False
            _LOGGER.exception(e)
        except ConnectionError as e:
            self._available = False
            _LOGGER.exception(e)
        except HTTPError as e:
            self._available = False
            _LOGGER.exception(e)
        except URLRequired as e:
            self._available = False
            _LOGGER.exception(e)
        except TooManyRedirects as e:
            self._available = False
            _LOGGER.exception(e)
        except ConnectTimeout as e:
            self._available = False
            _LOGGER.exception(e)
        except ReadTimeout as e:
            self._available = False
            _LOGGER.exception(e)
        except Timeout as e:
            self._available = False
            _LOGGER.exception(e)
        except JSONDecodeError as e:
            self._available = False
            _LOGGER.exception(e)


