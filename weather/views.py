from django.shortcuts import render
from django.db import connection
from .models import Weather, Prediction
import json
import pickle
import pandas as pd

def load_artifacts():
    with open('/home/lwwws/lclWeather/cron/artifacts.pkl', 'rb') as f:
        artifacts = pickle.load(f)
    
    return artifacts

def index(request):
    weather_data = json.dumps(list(Weather.objects.values('date', 'temperature', 'humidity', 'pressure')), default=str)

    predictions_for_today = Prediction.objects.order_by('-date')[:2]
    args = {'weather_data': weather_data}

    if len(predictions_for_today) == 2:
        args['next24h'] = predictions_for_today[1]
        args['next36h'] = predictions_for_today[0]

        artifacts = load_artifacts()

        for key, val in artifacts.items():
            if isinstance(val, pd.DataFrame):
                artifacts[key] = val.to_dict(orient='records')
        
        args['artifacts'] = artifacts
    
    return render(request, 'index.html', args)

# from django.shortcuts import render
# from django.db import connection
# from .models import Weather
# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64

# # Create your views here.

# def dictfetchall(cursor):
#     "Return all rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]
#     return [dict(zip(columns, row)) for row in cursor.fetchall()]

# def fetchWeather():
#     weather_data = Weather.objects.all()

#     date = []
#     temperature = []
#     humidity = []
#     pressure = []

#     for data in weather_data:
#         date.append(data.date)
#         temperature.append(data.temperature)
#         humidity.append(data.humidity)
#         pressure.append(data.pressure)
    
#     return {'date': date, 'temperature': temperature, 'humidity': humidity, 'pressure': pressure}

# def toBase64(plt):
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png') 
#     buffer.seek(0)

#     image_png = buffer.getvalue()
#     buffer.close()
#     return base64.b64encode(image_png).decode('utf-8')


# def index(request):
#     weather = fetchWeather()

#     plt.figure(figsize=(10, 5)) 
#     plt.plot(weather['date'], weather['temperature'], marker='o', linestyle='-', markersize=1, color='r')
#     plt.xlabel('Date')
#     plt.ylabel('Temperature')
#     plt.title('Temperature Over Time')

#     image_base64_temperature = toBase64(plt)


#     plt.figure(figsize=(10, 5)) 
#     plt.plot(weather['date'], weather['humidity'], marker='o', linestyle='-', markersize=1, color='b')
#     plt.xlabel('Date')
#     plt.ylabel('Humidity')
#     plt.title('Humidity Over Time')

#     image_base64_humidity = toBase64(plt)


#     plt.figure(figsize=(10, 5)) 
#     plt.plot(weather['date'], weather['pressure'], marker='o', linestyle='-', markersize=1, color='g')
#     plt.xlabel('Date')
#     plt.ylabel('Pressure')
#     plt.title('Pressure Over Time')

#     image_base64_pressure = toBase64(plt)


#     return render(request, 'index.html',
#      {'temperature_chart': image_base64_temperature,
#         'humidity_chart': image_base64_humidity,
#         'pressure_chart': image_base64_pressure})