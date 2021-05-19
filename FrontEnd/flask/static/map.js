// adapted from https://docs.mapbox.com/mapbox-gl-js/example/heatmap-layer/

mapboxgl.accessToken = 'pk.eyJ1IjoiamFtZXNzdW4wNCIsImEiOiJja283M2JvbTcxcmEwMnFtYjV6cHpyeG80In0.nsVmoAcXDwTlLA5dPlwlfA';

var map = map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [134.866944, -24.994167], // starting position [lng, lat]
    zoom: 4 // starting zoom
    });

map.on('load', function() {
    let locationData;
    
    $.ajax({
        url: "/map_data/location",
        type: "GET",
        dataType: "JSON",
        success: function(data){
            locationData = data;
            loadMap(locationData);
        }
    })
})

function loadMap(mapData) {
    map.addSource(
        "tweetLocations",{
            "type": "geojson",
            "data": mapData
        });

    map.addLayer({
        "id": "tweetHeatmap",
        "type": "heatmap",
        "source": "tweetLocations",
        "paint": {
            // 'heatmap-color': [
            //     'interpolate',
            //     ['linear'],
            //     ['heatmap-density'],
            //     0,
            //     'rgba(255, 255, 255, 0)',
            //     0.25,
            //     'rgb(226,227,251)',
            //     0.5,
            //     'rgb(187,202,249)',
            //     0.75,
            //     'rgb(134,180,246)',
            //     1,
            //     'rgb(29, 161, 242)'
            // ],
            'heatmap-radius': [
                'interpolate',
                ['linear'],
                ['zoom'],
                0,2,9,25
            ]
        }
    });
}