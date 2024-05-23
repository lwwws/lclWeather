var weatherData = JSON.parse('{{ weather_data|safe }}');

var dates = weatherData.map((item) => {item.date});
var temperatures = weatherData.map((item) => {item.temperature});
var humidities = weatherData.map((item) => {item.humidity});
var pressures = weatherData.map((item) => {item.pressure});

var colors = {
    temp: 'rgb(227, 66, 41)',
    hum: 'rgb(49, 134, 245)',
    press: 'rgb(120, 237, 81)'
};

var trace1 = {
    x: dates,
    y: temperatures,
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Temperature',
    line: { color: colors.temp },
    marker: { color: colors.temp }
};

var trace2 = {
    x: dates,
    y: humidities,
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Humidity',
    line: { color: colors.hum },
    marker: { color: colors.hum }
};

var trace3 = {
    x: dates,
    y: pressures,
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Pressure',
    line: { color: colors.press },
    marker: { color: colors.press }
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