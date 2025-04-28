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
    .command-text {background-color: #f5f5f5; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
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
        # Open in new browser tab
        webbrowser.open_new_tab(website_url)
        return True
    except Exception as e:
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
    elif "open google" in command:
        if open_website("https://www.google.com"):
            response = "Opening Google in a new tab"
            action_performed = True
    elif "open youtube" in command:
        if open_website("https://www.youtube.com"):
            response = "Opening YouTube in a new tab"
            action_performed = True
    elif "open facebook" in command:
        if open_website("https://www.facebook.com"):
            response = "Opening Facebook in a new tab"
            action_performed = True
    elif "open instagram" in command:
        if open_website("https://www.instagram.com"):
            response = "Opening Instagram in a new tab"
            action_performed = True
    elif "open twitter" in command:
        if open_website("https://www.twitter.com"):
            response = "Opening Twitter in a new tab"
            action_performed = True
    elif "open gmail" in command or "open email" in command:
        if open_website("https://mail.google.com"):
            response = "Opening Gmail in a new tab"
            action_performed = True
    elif "open linkedin" in command:
        if open_website("https://www.linkedin.com"):
            response = "Opening LinkedIn in a new tab"
            action_performed = True
    elif "open github" in command:
        if open_website("https://github.com"):
            response = "Opening GitHub in a new tab"
            action_performed = True
    elif "open chatgpt" in command or "open chat" in command or "open gpt" in command:
        if open_website("https://chat.openai.com"):
            response = "Opening ChatGPT in a new tab"
            action_performed = True
    elif "open edge" in command:
        if open_website("https://www.microsoft.com/edge"):
            response = "Opening Microsoft Edge in a new tab"
            action_performed = True
    elif "watch anime" in command or "open aniwatch" in command:
        if open_website("https://aniwatch.to"):
            response = "Opening Aniwatch in a new tab"
            action_performed = True
    elif "open streamlit" in command:
        if open_website("https://streamlit.io"):
            response = "Opening Streamlit in a new tab"
            action_performed = True
    elif "generate images" in command or "open ideogram" in command:
        if open_website("https://ideogram.ai"):
            response = "Opening Ideogram in a new tab"
            action_performed = True
    
    # Fallback response
    else:
        response = "I don't understand that command. Please try again."
    
    # Record response
    st.session_state.responses.append({"command": command, "response": response, "action": action_performed})
    return response, action_performed

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Main", "Time & Date", "Weather", "Websites"])

# Tab 1: Main Command Interface
with tab1:
    st.markdown("<h2 class='tab-subheader'>Voice Assistant</h2>", unsafe_allow_html=True)
    
    # Command input
    command_input = st.text_input("Enter your command:", key="main_command", 
                                  placeholder="Try 'What's the time?' or 'Open YouTube'")
    
    # Command execution
    if st.button("Execute Command", key="execute_main"):
        if command_input:
            result, action_performed = process_command(command_input)
            
            # Display result
            st.markdown(f"<div class='command-text'><b>Command:</b> {command_input}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='response-text'><b>Response:</b> {result}</div>", unsafe_allow_html=True)
            
            # For website commands, add an explicit link
            if "open" in command_input.lower() and action_performed:
                st.success("Website opened in a new tab!")
                
                # Extract the website URL
                website_name = command_input.lower().replace("open ", "").strip()
                
                # Map common website names to URLs
                website_mapping = {
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
                
                # Find matching URL
                for key, url in website_mapping.items():
                    if key in website_name:
                        st.markdown(f"<div class='response-text'>If the website didn't open automatically, [click here]({url})</div>", unsafe_allow_html=True)
                        break
    
    # Recent responses
    st.markdown("<h3>Recent Commands</h3>", unsafe_allow_html=True)
    
    for item in reversed(st.session_state.responses[-5:]):  # Show last 5 responses in reverse order
        st.markdown(f"<div class='command-text'><b>Command:</b> {item['command']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='response-text'><b>Response:</b> {item['response']}</div>", unsafe_allow_html=True)
        st.markdown("---")
    
    if st.button("Clear History", key="clear_history"):
        st.session_state.responses = []
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
    live_time = st.empty()
    live_date = st.empty()
    
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    live_time.markdown(f"<div class='response-text'>Current Time: {current_time}</div>", unsafe_allow_html=True)
    live_date.markdown(f"<div class='response-text'>Current Date: {current_date}</div>", unsafe_allow_html=True)

# Tab 3: Weather
with tab3:
    st.markdown("<h2 class='tab-subheader'>Weather Information</h2>", unsafe_allow_html=True)
    
    city_input = st.text_input("Enter city name:", key="city_input", value=st.session_state.current_city)
    
    if st.button("Get Weather", key="get_weather"):
        if city_input:
            st.session_state.current_city = city_input
            weather_result = get_weather(city_input)
            st.markdown(f"<div class='response-text'>{weather_result}</div>", unsafe_allow_html=True)
    
    # Quick city buttons
    st.markdown("<h3>Quick Cities</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
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

# Tab 4: Websites
with tab4:
    st.markdown("<h2 class='tab-subheader'>Quick Website Access</h2>", unsafe_allow_html=True)
    
    # Create 3 columns
    col1, col2, col3 = st.columns(3)
    
    # Column 1 - Social Media
    with col1:
        st.markdown("<h3>Social Media</h3>", unsafe_allow_html=True)
        if st.button("Open YouTube", key="open_youtube"):
            if open_website("https://www.youtube.com"):
                st.success("Opening YouTube in a new tab")
                st.markdown(f"<div class='response-text'>If YouTube didn't open, [click here](https://www.youtube.com)</div>", unsafe_allow_html=True)
        
        if st.button("Open Facebook", key="open_facebook"):
            if open_website("https://www.facebook.com"):
                st.success("Opening Facebook in a new tab")
                st.markdown(f"<div class='response-text'>If Facebook didn't open, [click here](https://www.facebook.com)</div>", unsafe_allow_html=True)
        
        if st.button("Open Twitter", key="open_twitter"):
            if open_website("https://www.twitter.com"):
                st.success("Opening Twitter in a new tab")
                st.markdown(f"<div class='response-text'>If Twitter didn't open, [click here](https://www.twitter.com)</div>", unsafe_allow_html=True)
        
        if st.button("Open Instagram", key="open_instagram"):
            if open_website("https://www.instagram.com"):
                st.success("Opening Instagram in a new tab")
                st.markdown(f"<div class='response-text'>If Instagram didn't open, [click here](https://www.instagram.com)</div>", unsafe_allow_html=True)
    
    # Column 2 - Work & Study
    with col2:
        st.markdown("<h3>Work & Study</h3>", unsafe_allow_html=True)
        if st.button("Open Google", key="open_google"):
            if open_website("https://www.google.com"):
                st.success("Opening Google in a new tab")
                st.markdown(f"<div class='response-text'>If Google didn't open, [click here](https://www.google.com)</div>", unsafe_allow_html=True)
        
        if st.button("Open Gmail", key="open_gmail"):
            if open_website("https://mail.google.com"):
                st.success("Opening Gmail in a new tab")
                st.markdown(f"<div class='response-text'>If Gmail didn't open, [click here](https://mail.google.com)</div>", unsafe_allow_html=True)
        
        if st.button("Open GitHub", key="open_github"):
            if open_website("https://github.com"):
                st.success("Opening GitHub in a new tab")
                st.markdown(f"<div class='response-text'>If GitHub didn't open, [click here](https://github.com)</div>", unsafe_allow_html=True)
        
        if st.button("Open LinkedIn", key="open_linkedin"):
            if open_website("https://www.linkedin.com"):
                st.success("Opening LinkedIn in a new tab")
                st.markdown(f"<div class='response-text'>If LinkedIn didn't open, [click here](https://www.linkedin.com)</div>", unsafe_allow_html=True)
    
    # Column 3 - Entertainment & Tools
    with col3:
        st.markdown("<h3>Entertainment & Tools</h3>", unsafe_allow_html=True)
        if st.button("Open ChatGPT", key="open_chatgpt"):
            if open_website("https://chat.openai.com"):
                st.success("Opening ChatGPT in a new tab")
                st.markdown(f"<div class='response-text'>If ChatGPT didn't open, [click here](https://chat.openai.com)</div>", unsafe_allow_html=True)
        
        if st.button("Open Aniwatch", key="open_aniwatch"):
            if open_website("https://aniwatch.to"):
                st.success("Opening Aniwatch in a new tab")
                st.markdown(f"<div class='response-text'>If Aniwatch didn't open, [click here](https://aniwatch.to)</div>", unsafe_allow_html=True)
        
        if st.button("Open Streamlit", key="open_streamlit"):
            if open_website("https://streamlit.io"):
                st.success("Opening Streamlit in a new tab")
                st.markdown(f"<div class='response-text'>If Streamlit didn't open, [click here](https://streamlit.io)</div>", unsafe_allow_html=True)
        
        if st.button("Open Ideogram", key="open_ideogram"):
            if open_website("https://ideogram.ai"):
                st.success("Opening Ideogram in a new tab")
                st.markdown(f"<div class='response-text'>If Ideogram didn't open, [click here](https://ideogram.ai)</div>", unsafe_allow_html=True)

# Add a note about browser permissions
st.markdown("""
---
**Important Note About Browser Functionality:**

When running this app:
1. Make sure pop-up blockers are disabled for this site
2. For best results, run this app locally using `streamlit run app.py`
3. If websites don't open automatically, use the provided backup links
4. Some browsers restrict automatic tab opening - Chrome and Firefox work best
""")
