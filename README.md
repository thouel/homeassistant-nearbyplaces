# homeassistant-nearbyplaces
A plugin to get opening dates and hours of places nearby.

## Configuration
- Set up your api_key for the [Places API](https://console.cloud.google.com/) in const.py
- Configure the refresh rate from Places API (2 weeks by default) in sensor.py, search for SCAN_INTERVAL
- Add the places you want to retrieve in configuration.yaml : see configuration.yaml.snippet for config example
- You need to give the placeId to search using Places API : you can get them once and for all [here](https://developers.google.com/maps/documentation/places/web-service/place-id?hl=fr)
- Create a new Card in your UI to display the sensor, see place-ui.json.example