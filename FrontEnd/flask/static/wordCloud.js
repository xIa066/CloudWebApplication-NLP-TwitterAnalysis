var imageArea = document.getElementById("wordclouds");
var allHTML = '<img id="allTweets" src="../static/images/all.png" alt="Word cloud for all Tweets">';
var cityHTML = '<div class="row"><div class="column"><h4>Melbourne</h4><img src="static/images/melbourne.png"></div><div class="column">    <h4>Sydney</h4>    <img src="static/images/sydney.png"></div><div class="column">    <h4>Canberra</h4>    <img src="static/images/canberra.png"></div></div><div class="row"><div class="column">    <h4>Brisbane</h4>    <img src="static/images/brisbane.png"></div><div class="column"><h4>Perth</h4><img src="static/images/perth.png"></div><div class="column"><h4>Adelaide</h4><img src="static/images/adelaide.png"></div></div>';

$('#wordCloudOption').change(function () {
    let option = $('#wordCloudOption').val();
    imageArea.innerHTML = "";

    if (option == "all") {
        $("#wordclouds").html(allHTML);
    } else if (option == "city") {
        $("#wordclouds").html(cityHTML);
    }

    // $.ajax({
    //     url: '/word_cloud_img/' + option,
    //     type: "GET",
    //     dataType: "text",
    //     success: function(data) {
    //         if (data == "all") {
    //             $("#wordclouds").html(allHTML);
    //         } else if (data == "city") {
    //             $("#wordclouds").html(cityHTML);
    //         } else {
    //             ;
    //         }
    //     }
    // })
})