import streamlit as st
import datetime
import requests
import webbrowser
import time

# Page configuration
st.set_page_config(
    page_title="Jarvis Assistant",
    page_icon="🤖",
    layout="wide"
)

# Basic styling
st.markdown("""
<style>
    .main-header {text-align: center; font-size: 2.5rem; margin-bottom: 1rem;}
    .tab-subheader {font-size: 1.5rem; margin-bottom: 1rem;}
    .response-text {background-color: #f0f7ff; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'current_city' not in st.session_state:
    st.session_state.current_city = "Bahawalpur"

# Header
st.markdown("<h1 class='main-header'>JARVIS Assistant</h1>", unsafe_allow_html=True)

# Function to get time
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"

# Function to get date
def get_date():
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {current_date}"

# Function to get weather
def get_weather(city):
    try:
        api_key = "47f5042f9812fe43a495b8daaf14ab5e"  # OpenWeatherMap API key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
        
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] == 200:
            main_data = data["main"]
            weather_data = data["weather"][0]
            
            temp = main_data["temp"]
            description = weather_data["description"]
            humidity = main_data["humidity"]
            
            return f"Weather in {city}: {description.capitalize()}, Temperature: {temp}°C, Humidity: {humidity}%"
        else:
            return f"Could not find weather data for {city}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

# Function to open website
def open_website(website_url):
    try:
        # This will open the URL in a new browser tab
        webbrowser.open_new_tab(website_url)
        return f"Opening {website_url}"
    except Exception as e:
        return f"Error opening website: {str(e)}"

# Function to process voice commands
def process_command(command):
    command = command.lower()
    response = ""
    
    # Time command
    if "time" in command:
        response = get_time()
    
    # Date command
    elif "date" in command:
        response = get_date()
    
    # Weather command
    elif "weather" in command:
        # Try to extract city name
        if "in " in command:
            parts = command.split("in ")
            if len(parts) > 1:
                city = parts[1].strip()
                st.session_state.current_city = city
                response = get_weather(city)
            else:
                response = get_weather(st.session_state.current_city)
        else:
            response = get_weather(st.session_state.current_city)
    
    # Website commands
    elif "open google" in command:
        open_website("https://www.google.com")
        response = "Opening Google"
    elif "open youtube" in command:
        open_website("https://www.youtube.com")
        response = "Opening YouTube"
    elif "open facebook" in command:
        open_website("https://www.facebook.com")
        response = "Opening Facebook"
    elif "open instagram" in command:
        open_website("https://www.instagram.com")
        response = "Opening Instagram"
    elif "open twitter" in command:
        open_website("https://www.twitter.com")
        response = "Opening Twitter"
    elif "open gmail" in command or "open email" in command:
        open_website("https://mail.google.com")
        response = "Opening Gmail"
    elif "open linkedin" in command:
        open_website("https://www.linkedin.com")
        response = "Opening LinkedIn"
    elif "open github" in command:
        open_website("https://github.com")
        response = "Opening GitHub"
    elif "open chatgpt" in command or "open chat" in command or "open gpt" in command:
        open_website("https://chat.openai.com")
        response = "Opening ChatGPT"
    elif "open edge" in command:
        open_website("https://www.microsoft.com/edge")
        response = "Opening Microsoft Edge"
    elif "watch anime" in command or "open aniwatch" in command:
        open_website("https://aniwatch.to")
        response = "Opening Aniwatch"
    elif "open streamlit" in command:
        open_website("https://streamlit.io")
        response = "Opening Streamlit"
    elif "generate images" in command or "open ideogram" in command:
        open_website("https://ideogram.ai")
        response = "Opening Ideogram"
    
    # Fallback response
    else:
        response = "I don't understand that command. Please try again."
    
    st.session_state.responses.append(response)
    return response

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Main", "Time & Date", "Weather", "Websites"])

# Tab 1: Main Command Interface
with tab1:
    st.markdown("<h2 class='tab-subheader'>Voice Assistant</h2>", unsafe_allow_html=True)
    
    # Command input
    command_input = st.text_input("Enter your command:", placeholder="Try 'What's the time?' or 'Open YouTube'")
    
    if st.button("Execute Command"):
        if command_input:
            result = process_command(command_input)
            st.markdown(f"<div class='response-text'><b>Command:</b> {command_input}<br><b>Response:</b> {result}</div>", unsafe_allow_html=True)
    
    # Recent responses
    st.markdown("<h3>Recent Responses</h3>", unsafe_allow_html=True)
    for response in st.session_state.responses[-5:]:  # Show last 5 responses
        st.markdown(f"<div class='response-text'>{response}</div>", unsafe_allow_html=True)
    
    if st.button("Clear History"):
        st.session_state.responses = []
        st.experimental_rerun()

# Tab 2: Time & Date
with tab2:
    st.markdown("<h2 class='tab-subheader'>Time & Date</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Get Current Time"):
            time_result = get_time()
            st.markdown(f"<div class='response-text'>{time_result}</div>", unsafe_allow_html=True)
    
    with col2:
        if st.button("Get Current Date"):
            date_result = get_date()
            st.markdown(f"<div class='response-text'>{date_result}</div>", unsafe_allow_html=True)
    
    # Current time display that auto-updates
    st.markdown("<h3>Live Clock</h3>", unsafe_allow_html=True)
    live_time = st.empty()
    live_date = st.empty()
    
    # This will only update when the page refreshes or when a button is clicked
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    live_time.markdown(f"<div class='response-text'>Current Time: {current_time}</div>", unsafe_allow_html=True)
    live_date.markdown(f"<div class='response-text'>Current Date: {current_date}</div>", unsafe_allow_html=True)

# Tab 3: Weather
with tab3:
    st.markdown("<h2 class='tab-subheader'>Weather Information</h2>", unsafe_allow_html=True)
    
    city_input = st.text_input("Enter city name:", value=st.session_state.current_city)
    
    if st.button("Get Weather"):
        if city_input:
            st.session_state.current_city = city_input
            weather_result = get_weather(city_input)
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)
    
    # Quick city buttons
    st.markdown("<h3>Quick Cities</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Bahawalpur"):
            weather_result = get_weather("Bahawalpur")
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)
    
    with col2:
        if st.button("Lahore"):
            weather_result = get_weather("Lahore")
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Karachi"):
            weather_result = get_weather("Karachi")
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)

# Tab 4: Websites
with tab4:
    st.markdown("<h2 class='tab-subheader'>Quick Website Access</h2>", unsafe_allow_html=True)
    
    # Create 3 columns
    col1, col2, col3 = st.columns(3)
    
    # Column 1 - Social Media
    with col1:
        st.markdown("<h3>Social Media</h3>", unsafe_allow_html=True)
        if st.button("Open YouTube"):
            open_website("https://www.youtube.com")
            st.success("Opening YouTube in a new tab")
        
        if st.button("Open Facebook"):
            open_website("https://www.facebook.com")
            st.success("Opening Facebook in a new tab")
        
        if st.button("Open Twitter"):
            open_website("https://www.twitter.com")
            st.success("Opening Twitter in a new tab")
        
        if st.button("Open Instagram"):
            open_website("https://www.instagram.com")
            st.success("Opening Instagram in a new tab")
    
    # Column 2 - Work & Study
    with col2:
        st.markdown("<h3>Work & Study</h3>", unsafe_allow_html=True)
        if st.button("Open Google"):
            open_website("https://www.google.com")
            st.success("Opening Google in a new tab")
        
        if st.button("Open Gmail"):
            open_website("https://mail.google.com")
            st.success("Opening Gmail in a new tab")
        
        if st.button("Open GitHub"):
            open_website("https://github.com")
            st.success("Opening GitHub in a new tab")
        
        if st.button("Open LinkedIn"):
            open_website("https://www.linkedin.com")
            st.success("Opening LinkedIn in a new tab")
    
    # Column 3 - Entertainment & Tools
    with col3:
        st.markdown("<h3>Entertainment & Tools</h3>", unsafe_allow_html=True)
        if st.button("Open ChatGPT"):
            open_website("https://chat.openai.com")
            st.success("Opening ChatGPT in a new tab")
        
        if st.button("Open Aniwatch"):
            open_website("https://aniwatch.to")
            st.success("Opening Aniwatch in a new tab")
        
        if st.button("Open Streamlit"):
            open_website("https://streamlit.io")
            st.success("Opening Streamlit in a new tab")
        
        if st.button("Open Ideogram"):
            open_website("https://ideogram.ai")
            st.success("Opening Ideogram in a new tab")

# Add a note about browser permissions
st.markdown("""
---
**Note:** For website links to open properly:
1. Make sure pop-up blockers are disabled for this site
2. The app needs to be running locally (using `streamlit run app.py`) for the webbrowser functionality to work properly
""")
