const CONFIGURATION = {
    "locations": [
      {
        "title": "I am here",
        "address1": "<your_address>",
        "address2": "<your_address>",
        "coords": { "lat": <your_coords>, "lng": <your_coords> },
        "placeId": "<your_place_ID>"
      }
    ],
    "mapOptions": {
      "center": { "lat": <your_coords>, "lng": <your_coords> },
      "fullscreenControl": true,
      "mapTypeControl": false,
      "streetViewControl": false,
      "zoom": 15,
      "zoomControl": true,
      "maxZoom": 17,
      "mapId": ""
    },
    "mapsApiKey": "<your_API_key>",
    "capabilities": {
      "input": false,
      "autocomplete": false,
      "directions": false,
      "distanceMatrix": false,
      "details": false,
      "actions": false
    }
  };  

document.addEventListener('DOMContentLoaded', async () => {
await customElements.whenDefined('gmpx-store-locator');
const locator = document.querySelector('gmpx-store-locator');
locator.configureFromQuickBuilder(CONFIGURATION);
});



