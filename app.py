import streamlit as st
import datetime
import requests
import plotly.graph_objs as go
import speech_recognition as sr
import pyttsx3
import geocoder

# ====================== CONFIG ======================
API_KEY = '47f5042f9812fe43a495b8daaf14ab5e'
BASE_WEATHER_URL = "http://api.openweathermap.org/data/2.5/"

# ====================== UTILITIES ======================
def get_user_location():
    """Auto-detect user's city using IP address."""
    g = geocoder.ip('me')
    if g.ok:
        return g.city
    else:
        return "Bahawalpur"

def get_current_weather(city: str) -> dict | None:
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
    except:
        return None

def get_forecast(city: str) -> list[dict] | None:
    try:
        url = f"{BASE_WEATHER_URL}forecast?q={city}&appid={API_KEY}&units=metric&cnt=24"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "200":
            return None

        forecast = []
        for item in data["list"][::8]:
            forecast.append({
                "date": datetime.datetime.fromtimestamp(item["dt"]).strftime("%A"),
                "temp": item["main"]["temp"],
                "description": item["weather"][0]["description"].capitalize(),
            })
        return forecast
    except:
        return None

def get_current_datetime():
    now = datetime.datetime.now()
    date_today = now.strftime("%B %d, %Y")
    time_now = now.strftime("%I:%M:%S %p")
    return date_today, time_now

def speak(text):
    """Make Jarvis speak"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's voice input"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak Now")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        st.success(f"✅ You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        st.error("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        st.error("Speech service is down.")
        return ""

def process_voice_command(query, city):
    """Process user's voice commands"""
    if "weather" in query:
        weather = get_current_weather(city)
        if weather:
            speak(f"The temperature in {city} is {weather['temperature']} degrees with {weather['description']}.")
            st.info(f"Temperature: {weather['temperature']}°C, Condition: {weather['description']}")
    elif "date" in query:
        date_today, _ = get_current_datetime()
        speak(f"Today's date is {date_today}")
        st.success(f"📅 Today's Date: {date_today}")
    elif "time" in query:
        _, time_now = get_current_datetime()
        speak(f"The current time is {time_now}")
        st.success(f"⏰ Current Time: {time_now}")
    elif "youtube" in query:
        speak("Opening YouTube")
        st.markdown("[Open YouTube](https://www.youtube.com)")
    elif "google" in query:
        speak("Opening Google")
        st.markdown("[Open Google](https://www.google.com)")
    else:
        speak("Sorry, I don't understand that command.")
        st.warning("Command not recognized.")

# ====================== MAIN ======================
def main():
    st.set_page_config(page_title="Jarvis Web Assistant", page_icon="🤖", layout="wide")
    st.title("🤖 Jarvis Web Assistant")

    st.caption("Speak or click to interact with Jarvis Assistant.")

    city = get_user_location()
    st.info(f"📍 Auto-Detected Location: **{city}**")

    theme = st.radio("Theme Mode:", ["Light", "Dark"], horizontal=True)
    if theme == "Dark":
        st.markdown("""
            <style>body {background-color: #0e1117; color: #fafafa;}</style>
        """, unsafe_allow_html=True)

    tabs = st.tabs(["🌦️ Weather", "⏰ Date & Time", "🗣️ Voice Assistant", "🌐 Quick Links"])

    # --- Weather Tab ---
    with tabs[0]:
        st.header("🌦️ Live Weather")

        weather = get_current_weather(city)
        forecast = get_forecast(city)

        if weather:
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature (°C)", f"{weather['temperature']}°C")
            col2.metric("Pressure (hPa)", weather['pressure'])
            col3.metric("Humidity (%)", weather['humidity'])
            st.success(f"**Condition:** {weather['description']}")
        else:
            st.error("Weather data unavailable.")

        st.subheader("📅 3-Day Forecast")

        if forecast:
            forecast_days = [item["date"] for item in forecast]
            forecast_temps = [item["temp"] for item in forecast]

            fig = go.Figure(go.Scatter(
                x=forecast_days,
                y=forecast_temps,
                mode='lines+markers',
                marker=dict(color='cyan', size=10),
                line=dict(color='royalblue', width=3)
            ))
            fig.update_layout(title="Temperature Trend (Next 3 Days)",
                              xaxis_title="Day",
                              yaxis_title="Temperature (°C)")
            st.plotly_chart(fig, use_container_width=True)

    # --- Date & Time Tab ---
    with tabs[1]:
        st.header("🗓️ Current Date and Time")
        date_today, time_now = get_current_datetime()

        st.subheader("📅 Date")
        st.success(date_today)

        st.subheader("⏰ Time")
        st.success(time_now)

    # --- Voice Assistant Tab ---
    with tabs[2]:
        st.header("🎙️ Voice Commands")
        if st.button("🎤 Start Listening"):
            query = listen()
            if query:
                process_voice_command(query, city)

    # --- Quick Links Tab ---
    with tabs[3]:
        st.header("🌐 Quick Access Websites")
        render_quick_links()

def render_quick_links():
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
        "🍿 Aniwatch": "https://aniwatch.to",
        "📈 Streamlit": "https://streamlit.io",
    }
    cols = st.columns(3)
    for idx, (name, url) in enumerate(websites.items()):
        with cols[idx % 3]:
            st.link_button(name, url)

# ====================== ENTRY ======================
if __name__ == "__main__":
    main()
