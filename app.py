import streamlit as st
from streamlit_js_eval import get_geolocation
from collections import defaultdict
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from history import init_db, read_records, create_record, delete_record, update_record
from helper import get_coordinates, get_weather, validate_coordinates, deg_to_compass

st.set_page_config(page_title="Weather App", layout="wide")
init_db()

st.markdown(
    """
    <style>
    .stButton > button {
        width: 200px;
        height: 40px;
        font-size: 16px;
        border-radius: 12px;
    }
    .weather-card {
        padding: 15px;
        border-radius: 15px;
        background-color: #f0f2f6;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col_top_left, col_top_right = st.columns([3, 1])
with col_top_right:
    if st.button("ℹ️ About PM Accelerator"):
        st.info(
            "PM Accelerator helps aspiring product managers become industry-ready by offering real-world training, mentorship, and job-focused guidance. Learn more at [Product Manager Accelerator](https://www.linkedin.com/school/pmaccelerator/)"
        )

tabs = st.tabs(["🏠 Home", "📜 History"])

with tabs[0]:
    st.markdown("<h1 style='text-align: center;'>☀️ Weather App</h1>", unsafe_allow_html=True)

    input_type = st.selectbox(
        "Choose how you want to enter the location:",
        ["City/Town", "Zip Code/Postal Code", "GPS Coordinates", "Landmarks", "Current location"]
    )

    def display_weather(lat, lon, location_label):
        weather_data = get_weather(lat, lon, "current")
        if weather_data:
            st.subheader(f"Current Weather — {location_label}")
            col1, col2, col3 = st.columns(3)

            avg_temp = weather_data["main"]["temp"]
            sky_condition = weather_data["weather"][0]["description"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            wind_deg = weather_data["wind"]["deg"]
            wind_dir = deg_to_compass(wind_deg)

            with col1:
                st.markdown(f"<div class='weather-card'><h4>🌡️ Temperature</h4><p>{avg_temp} °C</p></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='weather-card'><h4>☁️ Condition</h4><p>{sky_condition}</p></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='weather-card'><h4>💧 Humidity</h4><p>{humidity} %</p></div>", unsafe_allow_html=True)

            st.markdown(f"<div class='weather-card'><h4>🌬️ Wind</h4><p>{wind_speed} m/s, {wind_dir} ({wind_deg}°)</p></div>", unsafe_allow_html=True)

            create_record(location_label, avg_temp, sky_condition, humidity, wind_speed, wind_dir)

            forecast_data = get_weather(lat, lon, mode="forecast")
            if forecast_data:
                daily_forecast = defaultdict(list)
                for entry in forecast_data["list"]:
                    date = entry["dt_txt"].split(" ")[0]
                    daily_forecast[date].append(entry)

                st.subheader("📅 5-Day Forecast")
                forecast_summary = []
                for date, entries in list(daily_forecast.items())[:5]:
                    temps = [e["main"]["temp"] for e in entries]
                    descriptions = [e["weather"][0]["description"] for e in entries]
                    avg_temp = round(sum(temps) / len(temps), 2)
                    common_desc = max(set(descriptions), key=descriptions.count)
                    forecast_summary.append({"Date": date, "Temp": avg_temp, "Condition": common_desc})
                    st.write(f"{date} — 🌡️ {avg_temp}°C — {common_desc}")

                df_forecast = pd.DataFrame(forecast_summary)
                fig, ax = plt.subplots()
                ax.plot(df_forecast["Date"], df_forecast["Temp"], marker="o")
                ax.set_title("5-Day Temperature Trend")
                ax.set_ylabel("Temperature (°C)")
                st.pyplot(fig)

    if input_type in ["City/Town", "Zip Code/Postal Code", "Landmarks"]:
        user_input = st.text_input(f"### Enter the {input_type}")
        if user_input:
            lat, lon = get_coordinates(user_input)
            if lat is None or lon is None:
                st.error("Location not found. Please check the spelling or try again.")
            else:
                display_weather(lat, lon, user_input)

    elif input_type == "GPS Coordinates":
        coords = st.text_input("### Enter the GPS Coordinates in this format: (latitude, longitude)")
        if coords:
            lat, lon = validate_coordinates(coords)
            if lat is None or lon is None:
                st.error("Invalid coordinates. Format: (lat, lon) e.g. (28.61, 77.20)")
            else:
                display_weather(lat, lon, coords)

    else:
        location = get_geolocation()
        if location is None:
            st.info("Requesting location access...")
        elif "coords" in location:
            lat = location["coords"]["latitude"]
            lon = location["coords"]["longitude"]
            st.success(f"Location acquired: ({lat}, {lon})")
            display_weather(lat, lon, "Current Location")

with tabs[1]:
    st.title("📜 Weather History")

    record_id = st.text_input("Enter the ID of the record")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete Record"):
            delete_record(record_id)
            st.success("Record deleted successfully!")
    with col2:
        new_location = st.text_input("New Location")
        new_time = st.time_input("New Time")
        if st.button("Update Record"):
            if new_location and new_time:
                full_datetime = datetime.combine(datetime.today(), new_time)
                lat, lon = get_coordinates(new_location)
                if lat is None or lon is None:
                    st.error("Location not found.")
                else:
                    weather = get_weather(lat, lon, mode="current")
                    if weather:
                        wind_deg = weather["wind"]["deg"]
                        wind_dir = deg_to_compass(wind_deg)
                        update_record(
                            record_id,
                            new_location,
                            full_datetime,
                            weather['main']['temp'],
                            weather["weather"][0]["description"],
                            weather["main"]["humidity"],
                            weather["wind"]["speed"],
                            wind_dir
                        )
                        st.success("Record updated successfully!")

    history = read_records()
    if not history.empty:
        st.subheader("Past Weather Records")
        st.dataframe(history, use_container_width=True)

        if "Temperature" in history.columns:
            st.subheader("📊 Weather Trends from History")
            fig, ax = plt.subplots()
            ax.plot(history["Time"], history["Temperature"], marker="o", label="Temperature (°C)")
            ax.set_xlabel("Date")
            ax.set_ylabel("Temperature (°C)")
            ax.legend()
            st.pyplot(fig)

            if "Humidity" in history.columns:
                fig, ax = plt.subplots()
                ax.plot(history["Time"], history["Humidity"], marker="s", color="orange", label="Humidity (%)")
                ax.set_xlabel("Date")
                ax.set_ylabel("Humidity (%)")
                ax.legend()
                st.pyplot(fig)

            if "Wind Speed" in history.columns:
                fig, ax = plt.subplots()
                ax.plot(history["Time"], history["Wind Speed"], marker="^", color="green", label="Wind Speed (m/s)")
                ax.set_xlabel("Date")
                ax.set_ylabel("Wind Speed (m/s)")
                ax.legend()
                st.pyplot(fig)
    else:
        st.info("No history records found.")

st.markdown("<p style='text-align: center; font-size:14px;'>Developed by Ishan Shrivastava</p>", unsafe_allow_html=True)
