# homeassistant-nearbyplaces
A plugin to get opening dates and hours of places nearby.

## Whats does it do ?
It's a home-assistant sensor refreshing at a constant rate (see below SCAN_INTERVAL) from the Google Places API. You need to activate this API on your side and confgure the API_KEY (see below const.py).
Next you identify the places you want to retrieve and you will obtain one sensor per place after the next refresh.

## Configuration
- Set up your api_key for the [Places API](https://console.cloud.google.com/) in const.py
- Configure the refresh rate from Places API (2 weeks by default) in sensor.py, search for SCAN_INTERVAL
- Add the places you want to retrieve in configuration.yaml : see configuration.yaml.snippet for config example
- You need to give the placeId to search using Places API : you can get them once and for all [here](https://developers.google.com/maps/documentation/places/web-service/place-id?hl=fr)
- Create a new Card in your UI to display the sensor, see place-ui.json.example
