<script>
        // Convert Django context data to JavaScript
        var weatherData = {{ weather_data | safe }};
        
        var dates = weatherData.map(item => item.date);
        var temperatures = weatherData.map(item => item.temperature);
        var humidities = weatherData.map(item => item.humidity);
        var pressures = weatherData.map(item => item.pressure);

        var trace1 = {
            x: dates,
            y: temperatures,
            type: 'scatter',
            name: 'Temperature'
        };

        var trace2 = {
            x: dates,
            y: humidities,
            type: 'scatter',
            name: 'Humidity'
        };

        var trace3 = {
            x: dates,
            y: pressures,
            type: 'scatter',
            name: 'Pressure'
        };

        var data = [trace1, trace2, trace3];

        var layout = {
            title: 'Weather Data',
            xaxis: {
                title: 'Date'
            },
            yaxis: {
                title: 'Values'
            }
        };

        Plotly.newPlot('chart', data, layout);
    </script>