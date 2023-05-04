window.onload = function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    var months = [];
    var avgPrices = [];

    fetch('/data')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            months = data.months;
            avgPrices = data.avgPrices;

            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: months,
                    datasets: [{
                        label: '월 평균 감귤 가격',
                        data: avgPrices,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        })
        .catch(function(error) {
            console.log(error);
        });
}
