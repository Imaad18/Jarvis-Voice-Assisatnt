import streamlit as st
import datetime
import requests
import plotly.graph_objs as go

# ====================== CONFIGURATION ======================
CITY = "Bahawalpur"
API_KEY = '47f5042f9812fe43a495b8daaf14ab5e'
BASE_WEATHER_URL = "http://api.openweathermap.org/data/2.5/"

# ====================== UTILITY FUNCTIONS ======================
def get_current_weather(city: str = CITY) -> dict | None:
    """Fetch current weather information."""
    try:
        url = f"{BASE_WEATHER_URL}weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
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
        st.error(f"Error fetching current weather: {e}")
        return None

def get_forecast(city: str = CITY) -> list[dict] | None:
    """Fetch 3-day weather forecast."""
    try:
        url = f"{BASE_WEATHER_URL}forecast?q={city}&appid={API_KEY}&units=metric&cnt=24"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "200":
            return None

        forecast = []
        for item in data["list"][::8]:  # Every 8 intervals = approx. 1 day
            forecast.append({
                "date": datetime.datetime.fromtimestamp(item["dt"]).strftime("%A"),
                "temp": item["main"]["temp"],
                "description": item["weather"][0]["description"].capitalize(),
            })
        return forecast
    except Exception as e:
        st.error(f"Error fetching forecast: {e}")
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

def apply_custom_style():
    """Apply custom CSS for animations and hover effects."""
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            transition: background-color 0.3s;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #45a049;
            color: white;
        }
        .typing {
            font-size: 40px;
            font-weight: bold;
            animation: typing 4s steps(40, end), blink-caret .75s step-end infinite;
            white-space: nowrap;
            overflow: hidden;
            border-right: 3px solid;
            width: 100%;
        }
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: black; }
        }
        </style>
    """, unsafe_allow_html=True)

# ====================== MAIN APP ======================
def main():
    st.set_page_config(page_title="Jarvis Web", page_icon="🤖", layout="wide")
    apply_custom_style()

    st.markdown('<div class="typing">🤖 Welcome to Jarvis - Your Web Assistant!</div>', unsafe_allow_html=True)
    st.caption("Bringing you the latest weather, time, and quick access at one place.")

    theme = st.radio("Choose Theme Mode:", ["🌞 Light Mode", "🌜 Dark Mode"], horizontal=True)

    if theme == "🌜 Dark Mode":
        st.markdown("""
            <style>body {background-color: #0e1117; color: #fafafa;}</style>
        """, unsafe_allow_html=True)

    tabs = st.tabs(["🌦️ Weather", "⏰ Date & Time", "🌐 Quick Links"])

    # --- Weather Tab ---
    with tabs[0]:
        st.header("🌤️ Current Weather - Bahawalpur")

        weather = get_current_weather()
        forecast = get_forecast()

        if weather:
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature (°C)", f"{weather['temperature']}°C")
            col2.metric("Pressure (hPa)", weather['pressure'])
            col3.metric("Humidity (%)", weather['humidity'])
            st.success(f"**Condition:** {weather['description']}")
        else:
            st.error("❌ Unable to fetch current weather.")

        st.subheader("📅 3-Day Forecast")

        if forecast:
            forecast_days = [item["date"] for item in forecast]
            forecast_temps = [item["temp"] for item in forecast]

            # Forecast Table
            for day in forecast:
                st.info(f"{day['date']}: {day['description']} ({day['temp']}°C)")

            # Forecast Chart
            fig = go.Figure(go.Scatter(
                x=forecast_days, 
                y=forecast_temps,
                mode='lines+markers',
                marker=dict(color='blue', size=10),
                line=dict(color='royalblue', width=3)
            ))
            fig.update_layout(title="Temperature Trend (Next 3 Days)",
                              xaxis_title="Day",
                              yaxis_title="Temperature (°C)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Forecast data not available.")

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
