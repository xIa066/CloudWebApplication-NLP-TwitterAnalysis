// adapted from https://docs.mapbox.com/mapbox-gl-js/example/heatmap-layer/

const partyColours = {"LIB": "rgba(0, 71, 171, 0.5)", 
                      "ALP": "rgba(222, 53, 51, 0.5)", 
                      "GRN": "rgba(16, 194, 91, 0.5)"};

const heatmapLayer = {
    "id": "tweetHeatmap",
    "type": "heatmap",
    "source": "tweetLocations",
    "paint": {
        'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
            0,
            'rgba(68, 1, 84, 0)',
            0.2,
            'rgb(65, 68, 135)',
            0.4,
            'rgb(42, 120, 142)',
            0.6,
            'rgb(34, 168, 132)',
            0.8,
            'rgb(122, 209, 81)',
            1,
            'rgb(253, 213, 37)'
            ],
            
        'heatmap-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            0,2,9,25
        ]
    }
};

mapboxgl.accessToken = 'pk.eyJ1IjoiamFtZXNzdW4wNCIsImEiOiJja283M2JvbTcxcmEwMnFtYjV6cHpyeG80In0.nsVmoAcXDwTlLA5dPlwlfA';

var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [134.866944, -24.994167], // starting position [lng, lat]
    zoom: 4 // starting zoom
    });

map.on('load', function() {
    // load location data
    if (!sessionStorage.getItem('locationData')) {
        $.ajax({
            url: "/map_data/location",
            type: "GET",
            dataType: "JSON",
            success: function(data){
                map.addSource(
                    "tweetLocations",{
                        "type": "geojson",
                        "data": data
                    });
                sessionStorage.setItem('locationData', JSON.stringify(data));
                toggleHeatmap('default');
            }
        })
    } else {
        let locationData = JSON.parse(sessionStorage.getItem('locationData'));
        map.addSource(
            "tweetLocations",{
                "type": "geojson",
                "data": locationData
            });
        toggleHeatmap('default');
    }
    
    // load vote data
    if (!localStorage.getItem("voteData")) {
        $.ajax({
            url: "/map_data/vote",
            type: "GET",
            dataType: "JSON",
            success: function(data){
                map.addSource(
                    "voteCount",{
                        "type": "geojson",
                        "data": data
                    });
                localStorage.setItem('voteData', JSON.stringify(data));
            }
        })
    } else {
        let voteData = JSON.parse(localStorage.getItem('voteData'));
        map.addSource(
            "voteCount",{
                "type": "geojson",
                "data": voteData
            });
    }
});

function toggleHeatmap(checkbox) {
    if (checkbox.checked || checkbox == 'default') {
        let existingLayer = findExistingLayer();
        if (existingLayer) {
            map.addLayer(heatmapLayer, existingLayer);
        } else {
            map.addLayer(heatmapLayer);    
        }
    } else {
        map.removeLayer('tweetHeatmap');
    }
}

function toggleVoteCount(checkbox, party) {
    if (checkbox.checked) {
        map.addLayer({
            "id": party,
            "type": "circle",
            "source": "voteCount",
            "paint": {
                "circle-radius": [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    4,
                    ['interpolate', ['linear'], ['get', party], 10000, 1, 60000, 25],
                    9,
                    ['interpolate', ['linear'], ['get', party], 10000, 10, 60000, 100]
                ],
                "circle-stroke-color": "white",
                'circle-stroke-width': 1,
                "circle-color": partyColours[party]
            }
        });
    } else {
        map.removeLayer(party);
    }
}

function findExistingLayer() {
    let layers = map.getStyle().layers;
    for (var layer in layers) {
        if (layers[layer].type == "circle") {
            return layers[layer].id;
        }
    }
}