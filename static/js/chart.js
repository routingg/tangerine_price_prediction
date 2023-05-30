window.onload = function() {
    let ctx = document.getElementById('priceChart').getContext('2d');
    let months = [];
    let avgPrices = [];

    fetch('/get-price-data')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            months = data.months;
            avgPrices = data.avgPrices;

            let priceChart = new Chart(ctx, {
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
    fetch('/get-weather-data')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        let weatherCtx = document.getElementById('weatherChart').getContext('2d');

        let weatherChart = new Chart(weatherCtx, {
            type: 'bar',
            data: {
                labels: data.months,
                datasets: [
                    {
                        label: '월 평균 기온',
                        data: data.avgTemps,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    },
                    {
                        label: '월 평균 강수량',
                        data: data.avgRainfalls,
                        type: 'line',
                        fill: false,
                        borderColor: 'rgba(255, 159, 64, 1)',
                        borderWidth: 2
                    }
                ]
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
