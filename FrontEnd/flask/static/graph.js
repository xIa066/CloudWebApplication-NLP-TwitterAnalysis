const defaultMessage = '<span style="padding-left: 1%;">This page shows the average sentiment score of Tweets originating from particular cities in Australia over the past decade. Please choose an option from the menu above to view a graph.</span>';
let graph = document.getElementById("graph");

$("#graphOption").change(function (){
    let view = $("#graphOption").val();
    graph.innerHTML = "";

    $.ajax({
        url: "/graph_data/" + view,
        type: "GET",
        dataType: "html",
        success: function(data) {
           if (view != "none") {
               $("#graph").html(data);
           } else {
                $("#graph").html(defaultMessage);
           }
        },
        error: function(jqXHR, error) {
            alert("Sentiment score data could not be loaded.")
        }
    })
})