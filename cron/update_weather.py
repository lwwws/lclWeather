import smbus2
import bme280
import sqlite3
from datetime import datetime


def update_weather():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)

    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)
    data.temperature = round(data.temperature, 3)
    data.humidity = round(data.humidity, 3)
    data.pressure = round(data.pressure, 3)

    conn = None
    conn = sqlite3.connect('../db/weatherData.db')
    c = conn.cursor()
    now_str = (datetime.now()).strftime('%Y-%m-%d %H:%M')

    # Insert a row of data
    sql = '''INSERT INTO weather(date,temperature,humidity,pressure) VALUES (?,?,?,?)'''
    c.execute(sql, (now_str, data.temperature, data.humidity, data.pressure))

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    print("-- Inserted:")
    print(f"{now_str}\ntemp={data.temperature} c\nhumidity={data.humidity} %rH\npressure={data.pressure} hPa")


def main():
    update_weather()


if __name__ == '__main__':
    main()
