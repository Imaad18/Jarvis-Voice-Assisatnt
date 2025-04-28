import streamlit as st
import datetime
import requests
import time
import speech_recognition as sr

# ============ CUSTOM STYLING WITH ANIMATIONS ============
st.markdown("""
    <style>
    /* Global background settings */
    body {
        background-image: url('https://images.unsplash.com/photo-1604079628041-943cdece8a2f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80') !important;
        background-size: cover !important;
        background-attachment: fixed !important;
        background-position: center center !important;
        animation: fadeIn 2s ease-in-out; /* Fade-in effect for background */
    }
    
    /* Main app container with animation */
    .stApp {
        background-color: rgba(0,0,0,0.7) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        animation: slideIn 1s ease-out; /* Slide-in animation */
    }
    
    /* Button Styling with hover animation */
    .stButton>button {
        background-color: #0a84ff !important;
        color: white !important;
        border-radius: 8px !important;
        height: 3em !important;
        width: 100% !important;
        font-size: 18px !important;
        transition: transform 0.3s ease; /* Smooth transition */
    }
    .stButton>button:hover {
        background-color: #0066cc !important;
        color: #ffffff !important;
        transform: scale(1.05) !important; /* Button hover zoom */
    }
    
    /* Keyframes for Fade-in Animation */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    /* Keyframes for Slide-in Animation */
    @keyframes slideIn {
        0% { transform: translateY(30px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    /* Block container with backdrop effect */
    .block-container {
        backdrop-filter: blur(8px) saturate(150%) !important;
        background-color: rgba(17, 25, 40, 0.55) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        animation: fadeIn 2s ease-out; /* Fade-in for block container */
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #00ffff !important;
        animation: fadeIn 2s ease-in-out; /* Fade-in animation for headings */
    }
    
    /* Text */
    p, label, span {
        color: #e0e0e0 !important;
        animation: fadeIn 2s ease-in-out; /* Fade-in for text */
    }
    
    /* Links (button-like style for links) */
    .stLink a {
        color: #00ffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-decoration: none !important;
    }
    .stLink a:hover {
        color: #0066cc !important;
        text-decoration: underline !important;
    }
    </style>
""", unsafe_allow_html=True)

# ====================== WEATHER FUNCTION ======================
def get_weather():
    """Fetch weather information for Bahawalpur"""
    city = "Bahawalpur"
    api_key = '47f5042f9812fe43a495b8daaf14ab5e'  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] == "404":
        return None
    else:
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]
        
        return {
            "city": city,
            "description": description.capitalize(),
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity
        }

# ====================== SPEECH FUNCTION ======================
def listen_to_audio():
    """Record audio and return the text input"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak now!")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            st.write(f"You said: {query}")
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            st.error("Sorry, I couldn't reach the service.")
    return query

# ====================== MAIN APP ======================
def main():
    st.set_page_config(page_title="Jarvis Web", layout="wide")
    st.title("🤖 Jarvis - Your Web Assistant")
    
    tabs = st.tabs(["🌦️ Weather", "⏰ Date & Time", "🌐 Websites", "🎙️ Voice Input"])
    
    # --- Weather Tab ---
    with tabs[0]:
        st.header("Weather Information - Bahawalpur")
        st.spinner("Fetching weather data...")
        weather = get_weather()
        time.sleep(2)  # Simulating the loading time
        if weather:
            st.metric(label="Temperature (°C)", value=f"{weather['temperature']}°C")
            st.metric(label="Pressure (hPa)", value=weather['pressure'])
            st.metric(label="Humidity (%)", value=weather['humidity'])
            st.info(f"Condition: {weather['description']}")
        else:
            st.error("Could not fetch weather data. Please check your API key.")
    
    # --- Date & Time Tab ---
    with tabs[1]:
        st.header("Current Date and Time")
        now = datetime.datetime.now()
        date_today = now.strftime("%B %d, %Y")
        time_now = now.strftime("%I:%M:%S %p")
        
        st.subheader("📅 Date")
        st.success(date_today)
        
        st.subheader("⏰ Time")
        st.success(time_now)
    
    # --- Websites Tab ---
    with tabs[2]:
        st.header("Quick Access Websites")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.link_button("🔍 Google", "https://www.google.com")
            st.link_button("🎥 YouTube", "https://www.youtube.com")
            st.link_button("📘 Facebook", "https://www.facebook.com")
            st.link_button("📸 Instagram", "https://www.instagram.com")
        
        with col2:
            st.link_button("🐦 Twitter", "https://www.twitter.com")
            st.link_button("📧 Gmail", "https://mail.google.com")
            st.link_button("🔗 LinkedIn", "https://www.linkedin.com")
            st.link_button("🐙 GitHub", "https://github.com")
        
        with col3:
            st.link_button("🧠 ChatGPT", "https://chat.openai.com")
            st.link_button("🛡️ Microsoft Edge", "https://www.microsoft.com/edge")
            st.link_button("🍿 Aniwatch", "https://aniwatch.to")
            st.link_button("📈 Streamlit", "https://streamlit.io")
            st.link_button("🖼️ Ideogram", "https://ideogram.ai")
    
    # --- Voice Input Tab ---
    with tabs[3]:
        st.header("Voice Input")
        if st.button("Activate Jarvis"):
            st.write("Speak to Jarvis")
            query = listen_to_audio()
            st.write(f"Jarvis processed your query: {query}")

if __name__ == "__main__":
    main()
