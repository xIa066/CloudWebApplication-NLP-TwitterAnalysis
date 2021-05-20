// adapted from https://docs.mapbox.com/mapbox-gl-js/example/heatmap-layer/

mapboxgl.accessToken = 'pk.eyJ1IjoiamFtZXNzdW4wNCIsImEiOiJja283M2JvbTcxcmEwMnFtYjV6cHpyeG80In0.nsVmoAcXDwTlLA5dPlwlfA';

var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [134.866944, -24.994167], // starting position [lng, lat]
    zoom: 4 // starting zoom
    });

map.on('load', function() {
    if (!sessionStorage.getItem('locationData')) {
        $.ajax({
            url: "/map_data/location",
            type: "GET",
            dataType: "JSON",
            success: function(data){
                map.addSource(
                    "tweetLocations",{
                        "type": "geojson",
                        "data": mapData
                    });
                heatmap(data);
                sessionStorage.setItem('locationData', JSON.stringify(data));
            }
        })
    } else {
        let locationData = JSON.parse(sessionStorage.getItem('locationData'));
        heatmap(locationData);
    }
});

function heatmap(mapData) {
    map.addLayer({
        "id": "tweetHeatmap",
        "type": "heatmap",
        "source": "tweetLocations",
        "paint": {
            'heatmap-radius': [
                'interpolate',
                ['linear'],
                ['zoom'],
                0,2,9,25
            ]
        }
    });
}

function showVoteCount(party) {
    let voteData;

    if (!localStorage.getItem("voteData")) {
        $.ajax({
            url: "/aurin",
            type: "GET",
            dataType: "JSON",
            success: function(data){
                voteData = data;
                localStorage.setItem("voteData", JSON.stringify(data));
            }
        })
    } else {
        voteData = JSON.parse(localStorage.getItem("voteData"));
    }

    

    
}