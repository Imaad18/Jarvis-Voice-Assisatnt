import streamlit as st
import requests
import webbrowser
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# Set page config
st.set_page_config(page_title="Jarvis Assistant", page_icon="🤖", layout="wide")

# Title
st.markdown(
    "<h1 style='text-align: center; color: cyan;'>Jarvis AI - Streamlit Version</h1>",
    unsafe_allow_html=True
)

# Auto-refresh for the clock every 1 second
st_autorefresh(interval=1000, key="clockrefresh")

# Sidebar for Clock and User Info
with st.sidebar:
    st.header("🕒 Clock")
    current_time = datetime.now().strftime("%H:%M:%S")
    st.success(f"Current Time: {current_time}")

    st.header("👤 User")
    user = st.text_input("Enter your name", value="Guest")
    st.write(f"Welcome, {user}!")

# Define tabs (no "Main" tab now)
tabs = st.tabs(["Weather", "Websites", "YouTube", "About"])

# Weather Tab
with tabs[0]:
    st.header("🌤️ Weather Info")
    city_name = st.text_input("Enter City Name", "Bahawalpur")
    api_key = "6d50aa9cae6dc25b4cbb1fa0705c26eb"

    if st.button("Get Weather"):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description'].title()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            st.success(f"**Weather:** {weather}")
            st.info(f"**Temperature:** {temp}°C")
            st.warning(f"**Humidity:** {humidity}%")
            st.error(f"**Wind Speed:** {wind_speed} m/s")
        else:
            st.error("City not found!")

# Websites Tab
with tabs[1]:
    st.header("🌐 Open Websites")
    websites = {
        "Google": "https://www.google.com",
        "YouTube": "https://www.youtube.com",
        "GitHub": "https://www.github.com",
        "LinkedIn": "https://www.linkedin.com",
    }

    for name, url in websites.items():
        if st.button(f"Open {name}"):
            webbrowser.open_new_tab(url)  # Open in a new browser tab

# YouTube Tab
with tabs[2]:
    st.header("🎬 YouTube Search")
    search_query = st.text_input("Enter your search query", "")
    if st.button("Search on YouTube"):
        if search_query.strip() != "":
            youtube_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            webbrowser.open_new_tab(youtube_url)  # Open YouTube search in a new tab
        else:
            st.warning("Please enter a search query.")

# About Tab
with tabs[3]:
    st.header("ℹ️ About Jarvis AI")
    st.markdown(
        """
        - This is a simple AI Assistant built using **Streamlit**.
        - It can show **weather info**, **open websites**, and **search YouTube**.
        - Developed with ❤️ by [Your Name].
        """
    )
