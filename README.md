# Weather-App

A responsive weather forecast web app built using **Streamlit**, integrated with **OpenWeatherMap API** and **SQLite** for full CRUD (Create, Read, Update, Delete) operations and weather history storage.
The app allows users to search real-time weather conditions for any location worldwide and view detailed information like temperature, humidity, wind speed/direction, and sky conditions. It also includes a built-in system to save, view, update, and delete weather queries from history, giving users a persistent and editable weather log experience.

## 🚀 Features

- 🌍 **Real-Time Weather Search**: Enter any city/town name, Zip Code/Postal Code, GPS Coordinates, Landmarks, or use your **Current location** to fetch and display current weather data including temperature, sky condition, humidity, and wind details.
- 📊 **Interactive 5-Day Forecast**: Displays average daily temperature trends with a line chart along with textual summaries of sky conditions.
- 📋 **Weather History Log**: Automatically saves every search with location, time, and corresponding weather details into a local SQLite database.
- 🗑️ **Delete Records**: Allows users to delete specific entries from history by entering the record ID.
- ✏️ **Update Records**: Enables editing of a selected record’s location and time, with automatic weather update for the new values.
- 📈 **Visual History Trends**: Generates line charts for past queries (temperature, humidity, and wind speed) for better insights.
- 💾 **Persistent Storage**: Uses SQLite for durable data storage between sessions.
- 🧭 **Responsive and Intuitive UI**: Built using Streamlit’s modern UI components with tabs, styled cards, and charts.
- 🌐 **API Integrated**: Uses OpenWeatherMap API to fetch live and accurate weather data.


## 🧩 Tech Stack

- Streamlit
- SQLite
- geopy
- OpenWeatherMap API
- Pandas
- Matplotlib
- Python Standard Libraries: `datetime`, `requests`, `os`

## ⚙️ How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run weather_app_main.py
   ```


## 📁 Folder Structure
```
weather-app/
├── weather_app_main.py      # Main Streamlit app file
├── history_storer.py        # Handles SQLite operations
├── helper.py                # Utility functions for coordinates & weather
├── requirements.txt
├── weather.db               # Created automatically for history storage
└── README.md
```

## 🎨 UI/UX Enhancements
- Styled cards for displaying current weather details.
- Tab-based navigation (Home & History).
- Integrated line charts for forecast and historical trends.

## 📝 Note
```
Create a file named .streamlit/config.toml in the same directory as weather_app_main.py and add:

[theme]
base = "light"

This enables light mode for a cleaner visual experience.
```
