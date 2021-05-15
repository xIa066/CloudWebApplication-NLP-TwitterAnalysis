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
                graph.innerHTML = data;
           } else {

           }
        }
    })
})