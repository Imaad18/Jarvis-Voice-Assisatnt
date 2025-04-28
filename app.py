import streamlit as st
import datetime
import requests
import webbrowser
import time
import random

# Set page configuration
st.set_page_config(
    page_title="Jarvis Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #0066ff;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px #cccccc;
    }
    .subtitle {
        font-size: 1.3rem;
        color: #505050;
        text-align: center;
        margin-bottom: 2rem;
    }
    .response-box {
        background-color: #f0f7ff;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #0066ff;
    }
    .user-box {
        background-color: #f5f5f5;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #505050;
    }
    .stButton button {
        background-color: #0066ff;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        margin: 5px;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #0055cc;
    }
    /* Make text inputs larger */
    .stTextInput input {
        font-size: 1.2rem;
        padding: 1rem;
        border-radius: 10px;
    }
    /* Style the sidebar */
    .css-1d391kg {
        background-color: #f0f7ff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'greeting_done' not in st.session_state:
    st.session_state.greeting_done = False
if 'current_city' not in st.session_state:
    st.session_state.current_city = "Bahawalpur"

# Function to add messages to conversation history
def add_message(role, content):
    st.session_state.conversation.append({"role": role, "content": content})

# Function to speak (in web context, this just displays the message)
def speak(text):
    add_message("assistant", text)
    return text

# Function to open URL
def open_url(url_to_open):
    # Create a JavaScript script to open the URL in a new tab
    js = f"""
    <script>
        window.open('{url_to_open}', '_blank').focus();
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)
    return f"Opening {url_to_open}"

# Function to get weather information
def get_weather(city):
    """Fetch and return weather information"""
    try:
        # Use a free API key or store it securely
        api_key = "47f5042f9812fe43a495b8daaf14ab5e"  # Your OpenWeatherMap API key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
        
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] == 200:
            main_data = data["main"]
            weather_data = data["weather"][0]
            
            temp = main_data["temp"]
            humidity = main_data["humidity"]
            pressure = main_data["pressure"]
            description = weather_data["description"]
            
            weather_info = (
                f"Weather in {city}:\n"
                f"• Temperature: {temp}°C\n"
                f"• Weather: {description.capitalize()}\n"
                f"• Humidity: {humidity}%\n"
                f"• Atmospheric Pressure: {pressure} hPa"
            )
            return weather_info
        else:
            return f"Sorry, I couldn't find weather data for {city}. Please try another city."
    
    except Exception as e:
        return f"Sorry, I encountered an error getting weather data: {str(e)}"

# Function to get current time
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"

# Function to get current date
def get_date():
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {current_date}"

# Function to greet based on time of day
def greet():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    return f"{greeting} I'm Jarvis, your virtual assistant. How can I help you today?"

# Process commands
def process_command(command):
    # Convert command to lowercase for easier matching
    command = command.lower()
    
    # Time and date commands
    if any(word in command for word in ["time", "clock"]):
        return get_time()
    
    elif any(word in command for word in ["date", "day", "today"]):
        return get_date()
    
    # Weather commands
    elif "weather" in command:
        # Try to extract city name
        if "in " in command:
            parts = command.split("in ")
            if len(parts) > 1:
                city = parts[1].strip()
                st.session_state.current_city = city  # Save for future queries
                return get_weather(city)
        # Use default or previously mentioned city
        return get_weather(st.session_state.current_city)
    
    # Website commands - each will display a link and open a new tab
    elif "open google" in command:
        return "Opening Google", "https://www.google.com"
    elif "open youtube" in command:
        return "Opening YouTube", "https://www.youtube.com"
    elif "open facebook" in command:
        return "Opening Facebook", "https://www.facebook.com"
    elif "open instagram" in command:
        return "Opening Instagram", "https://www.instagram.com"
    elif "open twitter" in command or "open x" in command:
        return "Opening Twitter", "https://www.twitter.com"
    elif "open email" in command or "open gmail" in command:
        return "Opening Gmail", "https://mail.google.com"
    elif "open linkedin" in command:
        return "Opening LinkedIn", "https://www.linkedin.com"
    elif "open github" in command:
        return "Opening GitHub", "https://github.com"
    elif "open chat" in command or "open gpt" in command:
        return "Opening ChatGPT", "https://chat.openai.com"
    elif "open edge" in command:
        return "Opening Microsoft Edge", "https://www.microsoft.com/edge"
    elif "watch anime" in command or "open aniwatch" in command:
        return "Opening Aniwatch", "https://aniwatch.to"
    elif "open streamlit" in command:
        return "Opening Streamlit", "https://streamlit.io"
    elif "generate images" in command or "open ideogram" in command:
        return "Opening Ideogram", "https://ideogram.ai"
    
    # Help command
    elif "help" in command:
        help_text = """
        Here are some commands you can try:
        
        • "What time is it?" - Get the current time
        • "What's today's date?" - Get the current date
        • "What's the weather?" - Get weather for your city
        • "What's the weather in [city]?" - Get weather for any city
        • "Open [website]" - Open various websites like Google, YouTube, etc.
        • "Help" - Show this help message
        """
        return help_text
    
    # General queries that would go to a desktop assistant
    elif any(word in command for word in ["shutdown", "restart", "lock", "system"]):
        return "I'm sorry, I can't perform system operations in a web browser. This feature is only available in the desktop version."
    
    # Exit or goodbye commands
    elif any(word in command for word in ["bye", "exit", "quit", "goodbye"]):
        return random.choice([
            "Goodbye! It was nice assisting you. Refresh the page to start a new session.",
            "Have a great day! Refresh the page when you need my assistance again.",
            "Until next time! Refresh the page to start a new conversation."
        ])
    
    # If no command matches
    else:
        return "I'm not sure how to respond to that. Try asking for 'help' to see what I can do."

# Main application layout
st.markdown("<h1 class='main-title'>J.A.R.V.I.S</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Just A Rather Very Intelligent System</p>", unsafe_allow_html=True)

# Create columns for the main layout
col1, col2 = st.columns([2, 1])

# Main conversation area
with col1:
    st.subheader("Conversation")
    
    # Container for scrollable conversation history
    chat_container = st.container()
    
    # Display conversation history
    with chat_container:
        for message in st.session_state.conversation:
            if message["role"] == "user":
                st.markdown(f"<div class='user-box'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='response-box'><strong>Jarvis:</strong> {message['content']}</div>", unsafe_allow_html=True)
    
    # If this is the first load, show greeting
    if not st.session_state.greeting_done:
        greeting_msg = greet()
        speak(greeting_msg)
        st.session_state.greeting_done = True
    
    # Input area at the bottom
    user_input = st.text_input("Type your command...", key="command_input", 
                              placeholder="Try 'What's the weather?' or 'Open YouTube'")
    
    # Process user input when submitted
    if st.button("Send", key="send_button"):
        if user_input:
            # Add user message to conversation
            add_message("user", user_input)
            
            # Process the command
            result = process_command(user_input)
            
            # Handle website openings (tuple returns)
            if isinstance(result, tuple) and len(result) == 2:
                message, url = result
                speak(message)
                st.markdown(f"<div class='response-box'><strong>Jarvis:</strong> <a href='{url}' target='_blank'>Click here to open {url}</a></div>", unsafe_allow_html=True)
            else:
                speak(result)
            
            # Clear the input box (this requires a rerun)
            st.session_state.command_input = ""
            st.experimental_rerun()

# Sidebar with quick commands and info
with col2:
    st.sidebar.header("Quick Commands")
    
    # Time and Date
    if st.sidebar.button("📅 Check Date"):
        date_result = get_date()
        speak(date_result)
        st.experimental_rerun()
        
    if st.sidebar.button("⏰ Check Time"):
        time_result = get_time()
        speak(time_result)
        st.experimental_rerun()
    
    # Weather
    st.sidebar.subheader("Weather")
    weather_city = st.sidebar.text_input("City:", value=st.session_state.current_city)
    if st.sidebar.button("🌤️ Check Weather"):
        weather_result = get_weather(weather_city)
        st.session_state.current_city = weather_city
        speak(weather_result)
        st.experimental_rerun()
    
    # Popular websites
    st.sidebar.subheader("Quick Links")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("Google"):
            speak("Opening Google")
            st.markdown(f"<div class='response-box'><a href='https://www.google.com' target='_blank'>Click to open Google</a></div>", unsafe_allow_html=True)
            
        if st.button("YouTube"):
            speak("Opening YouTube")
            st.markdown(f"<div class='response-box'><a href='https://www.youtube.com' target='_blank'>Click to open YouTube</a></div>", unsafe_allow_html=True)
            
        if st.button("Gmail"):
            speak("Opening Gmail")
            st.markdown(f"<div class='response-box'><a href='https://mail.google.com' target='_blank'>Click to open Gmail</a></div>", unsafe_allow_html=True)
    
    with col2:
        if st.button("GitHub"):
            speak("Opening GitHub")
            st.markdown(f"<div class='response-box'><a href='https://github.com' target='_blank'>Click to open GitHub</a></div>", unsafe_allow_html=True)
            
        if st.button("ChatGPT"):
            speak("Opening ChatGPT")
            st.markdown(f"<div class='response-box'><a href='https://chat.openai.com' target='_blank'>Click to open ChatGPT</a></div>", unsafe_allow_html=True)
            
        if st.button("AniWatch"):
            speak("Opening AniWatch")
            st.markdown(f"<div class='response-box'><a href='https://aniwatch.to' target='_blank'>Click to open AniWatch</a></div>", unsafe_allow_html=True)
    
    # Help section
    st.sidebar.subheader("Need Help?")
    if st.sidebar.button("Show Help"):
        help_text = """
        Here are some commands you can try:
        
        • "What time is it?" - Get the current time
        • "What's today's date?" - Get the current date
        • "What's the weather?" - Get weather for your city
        • "What's the weather in [city]?" - Get weather for any city
        • "Open [website]" - Open various websites like Google, YouTube, etc.
        • "Help" - Show this help message
        """
        speak(help_text)
        st.experimental_rerun()
    
    # Clear conversation
    if st.sidebar.button("🗑️ Clear Conversation"):
        st.session_state.conversation = []
        st.session_state.greeting_done = False
        st.experimental_rerun()
