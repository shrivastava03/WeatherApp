import sqlite3
from datetime import datetime
import pandas as pd

def init_db():
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Location TEXT,
        Date_and_Time TEXT,
        Avg_Temperature_in_degree_C REAL,
        Sky_Condition TEXT,
        Humidity_in_percentage INTEGER,
        Wind_Speed_in_mps REAL,
        Wind_Direction TEXT
    )''')
    conn.commit()
    conn.close()


def read_records():
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("SELECT * FROM weather_data")
    data = c.fetchall()
    conn.close()
    columns = [desc[0] for desc in c.description]
    df = pd.DataFrame(data, columns=columns)
    return df

def create_record(location, avg_temperature, sky_condition, humidity, wind_speed, wind_direction):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = str(location)
    if isinstance(avg_temperature, tuple):
        avg_temperature = avg_temperature[0]
    avg_temperature = float(avg_temperature)

    sky_condition = str(sky_condition)
    if isinstance(humidity, tuple):
        humidity = humidity[0]
    humidity = int(humidity)
    wind_speed = float(wind_speed)
    wind_direction = str(wind_direction)

    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO weather_data (Location, Date_and_Time, Avg_Temperature_in_degree_C, Sky_Condition, Humidity_in_percentage, Wind_Speed_in_mps, Wind_Direction) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (location, date, avg_temperature, sky_condition, humidity, wind_speed, wind_direction)
    )
    conn.commit()
    conn.close()

def delete_record(record_id):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("DELETE FROM weather_data WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def update_record(record_id, location, date_time, avg_temperature, sky_condition, humidity, wind_speed, wind_direction):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("""
        UPDATE weather_data
        SET Location = ?, Date_and_Time = ?, Avg_Temperature_in_degree_C = ?, Sky_Condition = ?, Humidity_in_percentage = ?,Wind_Speed_in_mps = ?, Wind_Direction = ? WHERE Id = ?
    """,
        (location, date_time.strftime("%Y-%m-%d %H:%M:%S"), float(avg_temperature), sky_condition,
          int(humidity), float(wind_speed), wind_direction, int(record_id)))
    conn.commit()
    conn.close()