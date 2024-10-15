import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
from datetime import datetime, timedelta
import led

def fit_and_predict():
    led.setup_pins()
    led.turn_on(led.BLUE_PIN)

    conn = sqlite3.connect('/home/lwwws/lclWeather/db/weatherData')
    query = "SELECT * FROM weather"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # indexing df
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # lag values
    for lag in range(1, 6):
        df[f'temp_lag_{lag}'] = df['temperature'].shift(lag)
        df[f'hum_lag_{lag}'] = df['humidity'].shift(lag)
        df[f'press_lag_{lag}'] = df['pressure'].shift(lag)

    # avgs for 24 hours
    df['avg_temp_24h'] = df['temperature'].rolling(window=24).mean()
    df['avg_hum_24h'] = df['humidity'].rolling(window=24).mean()
    df['avg_press_24h'] = df['pressure'].rolling(window=24).mean()

    # Calculate rolling standard deviation
    df['temp_std_24h'] = df['temperature'].rolling(window=24).std()
    df['hum_std_24h'] = df['humidity'].rolling(window=24).std()
    df['press_std_24h'] = df['pressure'].rolling(window=24).std()

    # Interaction terms
    df['temp_hum_interaction'] = df['temperature'] * df['humidity']
    df['temp_press_interaction'] = df['temperature'] * df['pressure']
    df['hum_press_interaction'] = df['humidity'] * df['pressure']

    # Calculate differences between values 24 hours apart
    df['temp_diff_24h'] = df['temperature'].diff(periods=24)
    df['hum_diff_24h'] = df['humidity'].diff(periods=24)
    df['press_diff_24h'] = df['pressure'].diff(periods=24)

    # Get last row features
    last_row_features = df.iloc[[-1]]

    # Terms in next 24 hours
    df['temp_next24h'] = df['temperature'].shift(-24)
    df['hum_next24h'] = df['humidity'].shift(-24)
    df['press_next24h'] = df['pressure'].shift(-24)

    # Terms in next 24 hours
    df['temp_next24h'] = df['temperature'].shift(-24)
    df['hum_next24h'] = df['humidity'].shift(-24)
    df['press_next24h'] = df['pressure'].shift(-24)

    # Terms in next 36 hours
    df['temp_next36h'] = df['temperature'].shift(-36)
    df['hum_next36h'] = df['humidity'].shift(-36)
    df['press_next36h'] = df['pressure'].shift(-36)

    df.dropna(inplace=True)


    # Prepare train, test sets
    X = df.drop(['temp_next24h', 'hum_next24h', 'press_next24h', 'temp_next36h', 'hum_next36h', 'press_next36h'], axis=1)

    y_temp_24h = df['temp_next24h']
    y_hum_24h = df['hum_next24h']
    y_press_24h = df['press_next24h']

    y_temp_36h = df['temp_next36h']
    y_hum_36h = df['hum_next36h']
    y_press_36h = df['press_next36h']

    # Split the data for 24-hour predictions
    X_train_24h, X_test_24h, y_train_temp_24h, y_test_temp_24h = train_test_split(X, y_temp_24h, test_size=0.2, random_state=42)
    _, _, y_train_hum_24h, y_test_hum_24h = train_test_split(X, y_hum_24h, test_size=0.2, random_state=42)
    _, _, y_train_press_24h, y_test_press_24h = train_test_split(X, y_press_24h, test_size=0.2, random_state=42)

    # Train models for 24-hour predictions
    model_temp_24h = RandomForestRegressor(n_estimators=100, random_state=42)
    model_temp_24h.fit(X_train_24h, y_train_temp_24h)

    model_hum_24h = RandomForestRegressor(n_estimators=100, random_state=42)
    model_hum_24h.fit(X_train_24h, y_train_hum_24h)

    model_press_24h = RandomForestRegressor(n_estimators=100, random_state=42)
    model_press_24h.fit(X_train_24h, y_train_press_24h)

    models24h = {'temp':model_temp_24h,'hum':model_hum_24h,'press':model_press_24h}

    # Evaluate the models
    y_pred_temp_24h = model_temp_24h.predict(X_test_24h)
    rmse_temp_24h = mean_squared_error(y_test_temp_24h, y_pred_temp_24h, squared=False)

    y_pred_hum_24h = model_hum_24h.predict(X_test_24h)
    rmse_hum_24h = mean_squared_error(y_test_hum_24h, y_pred_hum_24h, squared=False)

    y_pred_press_24h = model_press_24h.predict(X_test_24h)
    rmse_press_24h = mean_squared_error(y_test_press_24h, y_pred_press_24h, squared=False)

    rmse24h = {'temp':rmse_temp_24h, 'hum': rmse_hum_24h, 'press':rmse_press_24h}

    print(f"24h Temperature RMSE: {rmse_temp_24h}")
    print(f"24h Humidity RMSE: {rmse_hum_24h}")
    print(f"24h Pressure RMSE: {rmse_press_24h}")


    # Repeat for 36-hour predictions
    X_train_36h, X_test_36h, y_train_temp_36h, y_test_temp_36h = train_test_split(X, y_temp_36h, test_size=0.2, random_state=42)
    _, _, y_train_hum_36h, y_test_hum_36h = train_test_split(X, y_hum_36h, test_size=0.2, random_state=42)
    _, _, y_train_press_36h, y_test_press_36h = train_test_split(X, y_press_36h, test_size=0.2, random_state=42)

    # Train models for 36-hour predictions
    model_temp_36h = RandomForestRegressor(n_estimators=100, random_state=42)
    model_temp_36h.fit(X_train_36h, y_train_temp_36h)

    model_hum_36h = RandomForestRegressor(n_estimators=100, random_state=42)
    model_hum_36h.fit(X_train_36h, y_train_hum_36h)

    model_press_36h = RandomForestRegressor(n_estimators=100, random_state=42)
    model_press_36h.fit(X_train_36h, y_train_press_36h)

    models36h = {'temp':model_temp_36h,'hum':model_hum_36h,'press':model_press_36h}

    # Evaluate the models
    y_pred_temp_36h = model_temp_36h.predict(X_test_36h)
    rmse_temp_36h = mean_squared_error(y_test_temp_36h, y_pred_temp_36h, squared=False)

    y_pred_hum_36h = model_hum_36h.predict(X_test_36h)
    rmse_hum_36h = mean_squared_error(y_test_hum_36h, y_pred_hum_36h, squared=False)

    y_pred_press_36h = model_press_36h.predict(X_test_36h)
    rmse_press_36h = mean_squared_error(y_test_press_36h, y_pred_press_36h, squared=False)

    rmse36h = {'temp':rmse_temp_36h, 'hum': rmse_hum_36h, 'press':rmse_press_36h}

    print(f"36h Temperature RMSE: {rmse_temp_36h}")
    print(f"36h Humidity RMSE: {rmse_hum_36h}")
    print(f"36h Pressure RMSE: {rmse_press_36h}")

    store(X, models24h, models36h, rmse24h, rmse36h, last_row_features)

    led.turn_off(led.BLUE_PIN)
    led.cleanup()

def store(X, models24h, models36h, rmse24h, rmse36h, last_row_features):
    artifacts = {
        'feature_importances_temp_24h': pd.DataFrame({
            'Feature': X.columns,
            'Importance': models24h['temp'].feature_importances_
            }).sort_values(by='Importance', ascending=False),
        'feature_importances_hum_24h': pd.DataFrame({
            'Feature': X.columns,
            'Importance': models24h['hum'].feature_importances_
            }).sort_values(by='Importance', ascending=False),
        'feature_importances_press_24h': pd.DataFrame({
            'Feature': X.columns,
            'Importance': models24h['press'].feature_importances_
            }).sort_values(by='Importance', ascending=False),
        'feature_importances_temp_36h': pd.DataFrame({
            'Feature': X.columns,
            'Importance': models36h['temp'].feature_importances_
            }).sort_values(by='Importance', ascending=False),
        'feature_importances_hum_36h': pd.DataFrame({
            'Feature': X.columns,
            'Importance': models36h['hum'].feature_importances_
            }).sort_values(by='Importance', ascending=False),
        'feature_importances_press_36h': pd.DataFrame({
            'Feature': X.columns,
            'Importance': models36h['press'].feature_importances_
            }).sort_values(by='Importance', ascending=False),
        'rmse24h': rmse24h,
        'rmse36h': rmse36h
    }

    with open('/home/lwwws/lclWeather/cron/artifacts.pkl', 'wb') as f:
        pickle.dump(artifacts, f)

    pred_temp_24h = models24h['temp'].predict(last_row_features)[0]
    pred_hum_24h = models24h['hum'].predict(last_row_features)[0]
    pred_press_24h = models24h['press'].predict(last_row_features)[0]
    pred_temp_36h = models36h['temp'].predict(last_row_features)[0]
    pred_hum_36h = models36h['hum'].predict(last_row_features)[0]
    pred_press_36h = models36h['press'].predict(last_row_features)[0]

    conn = None
    conn = sqlite3.connect('/home/lwwws/lclWeather/db/weatherData')
    c = conn.cursor()
    now_24h_str = (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M')
    now_36h_str = (datetime.now() + timedelta(hours=36)).strftime('%Y-%m-%d %H:%M')

    # Insert a row of data
    sql = '''INSERT INTO prediction(date,temperature,humidity,pressure) VALUES (?,?,?,?)'''
    c.execute(sql, (now_24h_str, pred_temp_24h, pred_hum_24h, pred_press_24h))
    c.execute(sql, (now_36h_str, pred_temp_36h, pred_hum_36h, pred_press_36h))

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def log_exception_to_file(exception):
    """Log the exception details to a file with a timestamped filename."""
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"/home/lwwws/lclWeather/cron/logs/error_log_{current_time}.txt"
    with open(file_path, "a") as file:
        file.write(f"Exception when fitting: {exception}\n")
        file.write(f"Exception type: {type(exception).__name__}\n\n")
    print(f"Exception details logged to: {file_path}")


def main():
    try:
        fit_and_predict()
        led.flash_twice(led.GREEN_PIN)
    except Exception as e:
        led.cleanup()
        log_exception_to_file(e)
        led.flash_heartbeat(led.RED_PIN)



if __name__ == '__main__':
    main()
