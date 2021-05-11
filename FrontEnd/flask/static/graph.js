var displayedGraph;

const barGraph = {
    type: 'bar',
    data: {
        labels: ['Melbourne', 'Canberra', 'Sydney', 'Brisbane'],
        datasets: [
            {
                label: 'Labour',
                data: [1,2,3,10],
                backgroundColor: 'red'
            },
            {
                label: 'Liberal',
                data: [1,2,3,2],
                backgroundColor: 'blue'
            },
            {
                label: 'Neutral',
                data: [5,3,10,2],         
                backgroundColor: 'gray'
            }
        ]
    }
};

$("#graphOption").change(function (){
    let graph = document.getElementById("graph").getContext('2d');
    let view = $("#graphOption").val();

    if (displayedGraph != null) {
        displayedGraph.destroy();
    }

    $.ajax({
        url: "/graph_data/" + view,
        type: "GET",
        dataType: "JSON",
        success: function(data) {
           if (view != "none") {
                // processSentimentData(data);

                displayedGraph = new Chart(graph, barGraph);
           } else {

           }
        }
    })
})

// function processSentimentData(sentimentData) {
//     let processedSentimentData = new Object();
//     let x;

//     for (x in sentimentData){
//         let xTemp = x;
//         x = x.replace(/'/g, '"');
//         x = JSON.parse(x);
        
//         city = x[0].split(", ")[0];
//         party = x[1];

//         let tempData = sentimentData[xTemp];
//         let avg = tempData['sum']/tempData['count'];
//     }

//     return processedSentimentData;
// }