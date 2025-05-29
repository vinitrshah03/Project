const CONFIGURATION = {
    "locations": [
      {
        "title": "I am here",
        "address1": "1, Atur Centre, Gokhale Rd, Model Colony",
        "address2": "Shivajinagar, Pune, Maharashtra 411016, India",
        "coords": { "lat": 18.5294, "lng": 73.8416 },
        "placeId": "ChIJm7p8MgXWwjsRBn06snOz95A"
      }
    ],
    "mapOptions": {
      "center": { "lat": 18.5294, "lng": 73.8416 },
      "fullscreenControl": true,
      "mapTypeControl": false,
      "streetViewControl": false,
      "zoom": 15,
      "zoomControl": true,
      "maxZoom": 17,
      "mapId": ""
    },
    "mapsApiKey": "AIzaSyCKreGefLNeCmau3sxt678RXFf5azvmQbg",
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



