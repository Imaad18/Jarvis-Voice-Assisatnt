import streamlit as st
import datetime
import requests
import webbrowser
import time
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="Jarvis Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh every second for the live clock
st_autorefresh(interval=1000, key="clock_refresh")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center; 
        font-size: 2.5rem; 
        margin-bottom: 1rem;
        color: #1a73e8;
    }
    .tab-subheader {
        font-size: 1.5rem; 
        margin-bottom: 1rem;
        color: #1a73e8;
    }
    .response-text {
        background-color: #f0f7ff; 
        padding: 1rem; 
        border-radius: 0.5rem; 
        margin: 1rem 0;
        border-left: 4px solid #1a73e8;
    }
    .command-text {
        background-color: #f5f5f5; 
        padding: 1rem; 
        border-radius: 0.5rem; 
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0d5bba;
        color: white;
    }
    .weather-icon {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    .success-box {
        background-color: #e6f4ea;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #34a853;
    }
    .error-box {
        background-color: #fce8e6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #d93025;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'current_city' not in st.session_state:
    st.session_state.current_city = "Bahawalpur"
if 'last_command' not in st.session_state:
    st.session_state.last_command = ""

# Header
st.markdown("<h1 class='main-header'>JARVIS Assistant</h1>", unsafe_allow_html=True)

# Function to get time
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"🕒 The current time is {current_time}"

# Function to get date
def get_date():
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"📅 Today is {current_date}"

# Function to get weather with emoji based on conditions
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
            
            # Add emoji based on weather condition
            weather_icon = "☀️"  # default
            if "cloud" in description.lower():
                weather_icon = "☁️"
            elif "rain" in description.lower():
                weather_icon = "🌧️"
            elif "snow" in description.lower():
                weather_icon = "❄️"
            elif "thunder" in description.lower():
                weather_icon = "⛈️"
            elif "clear" in description.lower():
                weather_icon = "☀️"
            
            return f"{weather_icon} Weather in {city}: {description.capitalize()}, Temperature: {temp}°C, Humidity: {humidity}%"
        else:
            return f"❌ Could not find weather data for {city}"
    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"

# Function to open website
def open_website(website_url):
    try:
        # Open in new browser tab
        webbrowser.open_new_tab(website_url)
        return True
    except Exception as e:
        st.error(f"Failed to open website: {str(e)}")
        return False

# Function to process voice commands
def process_command(command):
    command = command.lower()
    response = ""
    action_performed = False
    
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
    website_commands = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://www.twitter.com",
        "gmail": "https://mail.google.com",
        "email": "https://mail.google.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://github.com",
        "chatgpt": "https://chat.openai.com",
        "chat": "https://chat.openai.com",
        "gpt": "https://chat.openai.com",
        "edge": "https://www.microsoft.com/edge",
        "aniwatch": "https://aniwatch.to",
        "anime": "https://aniwatch.to",
        "streamlit": "https://streamlit.io",
        "ideogram": "https://ideogram.ai"
    }
    
    for site, url in website_commands.items():
        if f"open {site}" in command:
            if open_website(url):
                response = f"🌐 Opening {site.capitalize()} in a new tab"
                action_performed = True
                break
    
    # Fallback response
    if not response:
        response = "🤔 I don't understand that command. Try asking about time, weather, or to open a website."
    
    # Record response
    st.session_state.responses.append({"command": command, "response": response, "action": action_performed})
    st.session_state.last_command = command
    return response, action_performed

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Main", "Time & Date", "Weather", "Websites"])

# Tab 1: Main Command Interface
with tab1:
    st.markdown("<h2 class='tab-subheader'>Voice Assistant</h2>", unsafe_allow_html=True)
    
    # Command input with example commands
    command_input = st.text_input("Enter your command:", 
                                 key="main_command", 
                                 placeholder="Try 'What's the time?' or 'Open YouTube'",
                                 value=st.session_state.last_command)
    
    # Example commands
    with st.expander("Example Commands"):
        st.write("Try these commands:")
        col1, col2 = st.columns(2)
        with col1:
            st.write("- What time is it?")
            st.write("- What's the date today?")
            st.write("- Open Google")
            st.write("- Open YouTube")
        with col2:
            st.write("- What's the weather?")
            st.write("- Weather in Lahore")
            st.write("- Open ChatGPT")
            st.write("- Open Gmail")
    
    # Command execution
    if st.button("Execute Command", key="execute_main"):
        if command_input:
            result, action_performed = process_command(command_input)
            
            # Display result
            st.markdown(f"<div class='command-text'><b>Command:</b> {command_input}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='response-text'><b>Response:</b> {result}</div>", unsafe_allow_html=True)
            
            # For website commands, add an explicit link
            if "open" in command_input.lower() and action_performed:
                st.markdown("<div class='success-box'>Website opened in a new tab!</div>", unsafe_allow_html=True)
                
                # Extract the website name
                website_name = command_input.lower().replace("open ", "").strip()
                
                # Find matching URL
                for site, url in website_commands.items():
                    if site in website_name:
                        st.markdown(f"<div class='response-text'>If the website didn't open automatically, [click here to open {site.capitalize()}]({url})</div>", unsafe_allow_html=True)
                        break
    
    # Recent responses
    st.markdown("<h3>Recent Commands</h3>", unsafe_allow_html=True)
    
    if not st.session_state.responses:
        st.info("No commands executed yet. Try giving me a command!")
    else:
        for item in reversed(st.session_state.responses[-5:]):  # Show last 5 responses in reverse order
            st.markdown(f"<div class='command-text'><b>Command:</b> {item['command']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='response-text'><b>Response:</b> {item['response']}</div>", unsafe_allow_html=True)
            st.markdown("---")
    
    if st.button("Clear History", key="clear_history"):
        st.session_state.responses = []
        st.session_state.last_command = ""
        st.experimental_rerun()

# Tab 2: Time & Date
with tab2:
    st.markdown("<h2 class='tab-subheader'>Time & Date</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Get Current Time", key="get_time"):
            time_result = get_time()
            st.markdown(f"<div class='response-text'>{time_result}</div>", unsafe_allow_html=True)
    
    with col2:
        if st.button("Get Current Date", key="get_date"):
            date_result = get_date()
            st.markdown(f"<div class='response-text'>{date_result}</div>", unsafe_allow_html=True)
    
    # Current time display
    st.markdown("<h3>Live Clock</h3>", unsafe_allow_html=True)
    
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    st.markdown(f"<div class='response-text'>🕒 Current Time: {current_time}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='response-text'>📅 Current Date: {current_date}</div>", unsafe_allow_html=True)

# Tab 3: Weather
with tab3:
    st.markdown("<h2 class='tab-subheader'>Weather Information</h2>", unsafe_allow_html=True)
    
    city_input = st.text_input("Enter city name:", 
                              key="city_input", 
                              value=st.session_state.current_city,
                              help="Enter a city name to get weather information")
    
    if st.button("Get Weather", key="get_weather"):
        if city_input:
            st.session_state.current_city = city_input
            weather_result = get_weather(city_input)
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)
        else:
            st.error("Please enter a city name")
    
    # Quick city buttons
    st.markdown("<h3>Quick Cities</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Bahawalpur", key="city_bahawalpur"):
            weather_result = get_weather("Bahawalpur")
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)
    
    with col2:
        if st.button("Lahore", key="city_lahore"):
            weather_result = get_weather("Lahore")
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Karachi", key="city_karachi"):
            weather_result = get_weather("Karachi")
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)
    
    with col4:
        if st.button("Islamabad", key="city_islamabad"):
            weather_result = get_weather("Islamabad")
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)

# Tab 4: Websites
with tab4:
    st.markdown("<h2 class='tab-subheader'>Quick Website Access</h2>", unsafe_allow_html=True)
    
    # Create 3 columns
    col1, col2, col3 = st.columns(3)
    
    # Column 1 - Social Media
    with col1:
        st.markdown("<h3>🌐 Social Media</h3>", unsafe_allow_html=True)
        
        if st.button("YouTube", key="open_youtube"):
            if open_website("https://www.youtube.com"):
                st.markdown("<div class='success-box'>Opening YouTube in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If YouTube didn't open, [click here](https://www.youtube.com)</div>", unsafe_allow_html=True)
        
        if st.button("Facebook", key="open_facebook"):
            if open_website("https://www.facebook.com"):
                st.markdown("<div class='success-box'>Opening Facebook in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If Facebook didn't open, [click here](https://www.facebook.com)</div>", unsafe_allow_html=True)
        
        if st.button("Twitter", key="open_twitter"):
            if open_website("https://www.twitter.com"):
                st.markdown("<div class='success-box'>Opening Twitter in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If Twitter didn't open, [click here](https://www.twitter.com)</div>", unsafe_allow_html=True)
        
        if st.button("Instagram", key="open_instagram"):
            if open_website("https://www.instagram.com"):
                st.markdown("<div class='success-box'>Opening Instagram in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If Instagram didn't open, [click here](https://www.instagram.com)</div>", unsafe_allow_html=True)
    
    # Column 2 - Work & Study
    with col2:
        st.markdown("<h3>💼 Work & Study</h3>", unsafe_allow_html=True)
        
        if st.button("Google", key="open_google"):
            if open_website("https://www.google.com"):
                st.markdown("<div class='success-box'>Opening Google in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If Google didn't open, [click here](https://www.google.com)</div>", unsafe_allow_html=True)
        
        if st.button("Gmail", key="open_gmail"):
            if open_website("https://mail.google.com"):
                st.markdown("<div class='success-box'>Opening Gmail in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If Gmail didn't open, [click here](https://mail.google.com)</div>", unsafe_allow_html=True)
        
        if st.button("GitHub", key="open_github"):
            if open_website("https://github.com"):
                st.markdown("<div class='success-box'>Opening GitHub in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If GitHub didn't open, [click here](https://github.com)</div>", unsafe_allow_html=True)
        
        if st.button("LinkedIn", key="open_linkedin"):
            if open_website("https://www.linkedin.com"):
                st.markdown("<div class='success-box'>Opening LinkedIn in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If LinkedIn didn't open, [click here](https://www.linkedin.com)</div>", unsafe_allow_html=True)
    
    # Column 3 - Entertainment & Tools
    with col3:
        st.markdown("<h3>🎮 Entertainment & Tools</h3>", unsafe_allow_html=True)
        
        if st.button("ChatGPT", key="open_chatgpt"):
            if open_website("https://chat.openai.com"):
                st.markdown("<div class='success-box'>Opening ChatGPT in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If ChatGPT didn't open, [click here](https://chat.openai.com)</div>", unsafe_allow_html=True)
        
        if st.button("Aniwatch", key="open_aniwatch"):
            if open_website("https://aniwatch.to"):
                st.markdown("<div class='success-box'>Opening Aniwatch in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If Aniwatch didn't open, [click here](https://aniwatch.to)</div>", unsafe_allow_html=True)
        
        if st.button("Streamlit", key="open_streamlit"):
            if open_website("https://streamlit.io"):
                st.markdown("<div class='success-box'>Opening Streamlit in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If Streamlit didn't open, [click here](https://streamlit.io)</div>", unsafe_allow_html=True)
        
        if st.button("Ideogram", key="open_ideogram"):
            if open_website("https://ideogram.ai"):
                st.markdown("<div class='success-box'>Opening Ideogram in a new tab</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-text'>If Ideogram didn't open, [click here](https://ideogram.ai)</div>", unsafe_allow_html=True)

# Sidebar with app info
with st.sidebar:
    st.markdown("## About JARVIS")
    st.markdown("""
    JARVIS is your personal voice assistant that can:
    - Tell you the current time and date
    - Provide weather information
    - Open websites with a single command
    """)
    
    st.markdown("### How to Use")
    st.markdown("""
    1. Type your command in the input box
    2. Click "Execute Command"
    3. View the response
    """)
    
    st.markdown("### Browser Note")
    st.markdown("""
    For website opening to work:
    - Allow pop-ups for this site
    - Run the app locally for best results
    - Use Chrome or Firefox
    """)
    
    st.markdown("---")
    st.markdown("Created with ❤️ using Streamlit")

# Add a footer
st.markdown("""
---
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    JARVIS Assistant v1.0 • Made with Streamlit • © 2023
</div>
""", unsafe_allow_html=True)
