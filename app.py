import streamlit as st
import datetime
import requests

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

# ====================== MAIN APP ======================
def main():
    st.set_page_config(page_title="Jarvis Web", layout="wide")
    st.title("🤖 Jarvis - Your Web Assistant")
    
    tabs = st.tabs(["🌦️ Weather", "⏰ Date & Time", "🌐 Websites"])
    
    # --- Weather Tab ---
    with tabs[0]:
        st.header("Weather Information - Bahawalpur")
        weather = get_weather()
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
    
if __name__ == "__main__":
    main()

