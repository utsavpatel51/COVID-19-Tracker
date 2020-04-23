Chart.defaults.global.responsive = false
function minichart(label, values, canvas, borderC){
    var chartData = {
        labels : label,
        datasets: [{
            label: "",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: borderC,
            pointRadius: 0.5,
            pointHoverBorderWidth: 2,
            pointHoverRadius: 3,
            pointBorderColor : borderC,
            pointBackgroundColor: "#fff",                
            data: values,
            spanGaps: false
        }]
    }
    var ctx = document.getElementById(canvas).getContext("2d");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            tooltips: {
            enabled: true,
            mode: 'single',
            callbacks: {
                label: function(tooltipItems, data){
                    return tooltipItems.yLabel + ' case';
                }
            }
            },
            legend:{
                display: false
            },
            scales: 
            {
                yAxes: [{
                    ticks: {
                        display: false,
                    },
                    gridLines: {
                        display: false
                    }
                }],
                xAxes: [{
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        display: false
                    }
                }]
            }
        }
    })
}