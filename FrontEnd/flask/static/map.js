var map;

function initMap() {
    mapboxgl.accessToken = 'pk.eyJ1IjoiamFtZXNzdW4wNCIsImEiOiJja283M2JvbTcxcmEwMnFtYjV6cHpyeG80In0.nsVmoAcXDwTlLA5dPlwlfA';

    map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [134.866944, -24.994167], // starting position [lng, lat]
    zoom: 4 // starting zoom
    });
}

function displayHeatMap() {
    let locationData;

    $.ajax({
        url: "/map_data/loc",
        type: "GET",
        dataType: "JSON",
        success: function(data){
           console.log(data);
        }
    })

    map.addSource(
        "tweetLocations",{
            "type": "geojson",
            "data": locationData
        }
    )
}

function showSentiment() {
    return;
}