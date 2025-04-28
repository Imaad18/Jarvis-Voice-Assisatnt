import streamlit as st
import datetime
import requests

# ====================== CONFIGURATION ======================
CITY = "Bahawalpur"
API_KEY = '47f5042f9812fe43a495b8daaf14ab5e'  # Insert your OpenWeatherMap API key
BASE_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?"

# ====================== UTILITY FUNCTIONS ======================
def get_weather(city: str = CITY) -> dict | None:
    """Fetch current weather information for a given city."""
    try:
        complete_url = f"{BASE_WEATHER_URL}q={city}&appid={API_KEY}&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        if data.get("cod") != 200:
            return None
        
        main = data["main"]
        weather = data["weather"][0]

        return {
            "city": city,
            "description": weather["description"].capitalize(),
            "temperature": main["temp"],
            "pressure": main["pressure"],
            "humidity": main["humidity"],
        }
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def get_current_datetime() -> tuple[str, str]:
    """Get the current date and time formatted."""
    now = datetime.datetime.now()
    date_today = now.strftime("%B %d, %Y")
    time_now = now.strftime("%I:%M:%S %p")
    return date_today, time_now

def render_website_links():
    """Render a grid of quick-access website buttons."""
    websites = {
        "🔍 Google": "https://www.google.com",
        "🎥 YouTube": "https://www.youtube.com",
        "📘 Facebook": "https://www.facebook.com",
        "📸 Instagram": "https://www.instagram.com",
        "🐦 Twitter": "https://www.twitter.com",
        "📧 Gmail": "https://mail.google.com",
        "🔗 LinkedIn": "https://www.linkedin.com",
        "🐙 GitHub": "https://github.com",
        "🧠 ChatGPT": "https://chat.openai.com",
        "🛡️ Microsoft Edge": "https://www.microsoft.com/edge",
        "🍿 Aniwatch": "https://aniwatch.to",
        "📈 Streamlit": "https://streamlit.io",
        "🖼️ Ideogram": "https://ideogram.ai",
    }
    
    cols = st.columns(3)
    for idx, (name, url) in enumerate(websites.items()):
        with cols[idx % 3]:
            st.link_button(name, url)

# ====================== MAIN APP ======================
def main():
    st.set_page_config(page_title="Jarvis Web", page_icon="🤖", layout="wide")
    st.title("🤖 Jarvis - Your Personal Web Assistant")
    st.caption("Effortless Information at Your Fingertips!")

    tabs = st.tabs(["🌦️ Weather", "⏰ Date & Time", "🌐 Quick Links"])

    # --- Weather Tab ---
    with tabs[0]:
        st.header("🌤️ Current Weather - Bahawalpur")
        weather = get_weather()
        if weather:
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature (°C)", f"{weather['temperature']}°C")
            col2.metric("Pressure (hPa)", weather['pressure'])
            col3.metric("Humidity (%)", weather['humidity'])
            st.success(f"**Condition:** {weather['description']}")
        else:
            st.error("❌ Unable to fetch weather data. Please check your API key or try again later.")

    # --- Date & Time Tab ---
    with tabs[1]:
        st.header("🗓️ Current Date & Time")
        date_today, time_now = get_current_datetime()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📅 Date")
            st.success(date_today)
        
        with col2:
            st.subheader("⏰ Time")
            st.success(time_now)

    # --- Quick Links Tab ---
    with tabs[2]:
        st.header("🌐 Quick Access Websites")
        render_website_links()

# ====================== ENTRY POINT ======================
if __name__ == "__main__":
    main()
