import streamlit as st
import datetime
import requests
import base64
import time

# Set page configuration
st.set_page_config(
    page_title="Jarvis Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# CSS for custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .response-area {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .command-button {
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'listening' not in st.session_state:
    st.session_state.listening = False

# Function to simulate speech
def speak(text):
    st.session_state.messages.append({"role": "assistant", "content": text})
    return text

# Weather function
def get_weather(city="Bahawalpur"):
    """Fetch weather information"""
    try:
        api_key = st.secrets.get("OPENWEATHER_API_KEY", "47f5042f9812fe43a495b8daaf14ab5e")  # Ideally stored in secrets
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
        
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] == "404":
            return f"City {city} not found."
        else:
            main = data["main"]
            weather = data["weather"][0]
            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            description = weather["description"]
            
            return f"The weather in {city} is {description}. The temperature is {temperature}°C with a pressure of {pressure} hPa and humidity of {humidity}%."
    except Exception as e:
        return f"Unable to fetch weather: {str(e)}"

# Function to get time
def get_time():
    """Get current time"""
    return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"

# Function to get date
def get_date():
    """Get current date"""
    return f"Today is {datetime.datetime.now().strftime('%B %d, %Y')}"

# Function to process voice/text input
def process_command(command):
    """Process user commands"""
    if not command:
        return "I didn't catch that. Please try again."
    
    command = command.lower()
    
    # Time/Date Commands
    if 'time' in command:
        return get_time()
    elif 'date' in command:
        return get_date()
    
    # Weather Command
    elif 'weather' in command:
        city = "Bahawalpur"  # Default city
        # Try to extract city name if provided
        words = command.split()
        if "in" in words:
            try:
                city_index = words.index("in") + 1
                if city_index < len(words):
                    city = words[city_index]
            except:
                pass
        return get_weather(city)
    
    # Website Commands
    elif 'open google' in command:
        return "Opening Google in a new tab", "https://www.google.com"
    elif 'open youtube' in command:
        return "Opening YouTube in a new tab", "https://www.youtube.com"
    elif 'open facebook' in command:
        return "Opening Facebook in a new tab", "https://www.facebook.com"
    elif 'open instagram' in command:
        return "Opening Instagram in a new tab", "https://www.instagram.com"
    elif 'open twitter' in command:
        return "Opening Twitter in a new tab", "https://www.twitter.com"
    elif 'open email' in command or 'open gmail' in command:
        return "Opening Gmail in a new tab", "https://mail.google.com"
    elif 'open linkedin' in command:
        return "Opening LinkedIn in a new tab", "https://www.linkedin.com"
    elif 'open github' in command:
        return "Opening GitHub in a new tab", "https://www.github.com"
    elif 'open chat' in command or 'open gpt' in command:
        return "Opening ChatGPT in a new tab", "https://chat.openai.com"
    elif 'open microsoft edge' in command:
        return "Opening Microsoft Edge in a new tab", "https://www.microsoft.com/edge"
    elif 'watch anime' in command:
        return "Opening Aniwatch in a new tab", "https://aniwatch.to"
    elif 'open streamlit' in command:
        return "Opening Streamlit in a new tab", "https://streamlit.io"
    elif 'generate images' in command:
        return "Opening Ideogram in a new tab", "https://ideogram.ai"
    
    # System commands that won't work in Streamlit
    elif any(cmd in command for cmd in ['shutdown', 'restart', 'lock system']):
        return "I'm sorry, I can't perform system operations in a web environment."
    
    # Exit command
    elif 'exit' in command or 'quit' in command or 'bye' in command:
        return "Goodbye! You can close this tab or refresh to start a new session."
    
    # Fallback
    else:
        return "I didn't understand that command. Please try again."

# Display header
st.markdown("<h1 class='main-header'>Jarvis Voice Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Your AI assistant powered by Streamlit</p>", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.header("About Jarvis")
    st.info("Jarvis is a voice-controlled assistant that can help with time, date, weather, and opening websites.")
    
    st.header("Available Commands")
    st.markdown("""
    - Ask for time
    - Ask for date
    - Check weather
    - Open websites (Google, YouTube, etc.)
    - Say goodbye
    """)
    
    st.header("Voice Input")
    # Use microphone input (browser API)
    if st.button("Start Listening", key="listen"):
        st.session_state.listening = True
        st.warning("Microphone functionality requires JavaScript integration. For this demo, please use the text input below.")
        # In a real implementation, you would use Streamlit Components to integrate JS for mic access
        time.sleep(2)  # Simulate listening
        st.session_state.listening = False

# Main interface
col1, col2 = st.columns([3, 1])

# Text input for commands
with col1:
    user_input = st.text_input("Type your command:", placeholder="Try 'What's the time?' or 'Check weather'")

with col2:
    if st.button("Send", key="send_command"):
        if user_input:
            # Process the command
            result = process_command(user_input)
            
            # Handle website openings
            if isinstance(result, tuple) and len(result) == 2:
                message, url = result
                speak(message)
                st.markdown(f"[Click here to open]({url})", unsafe_allow_html=True)
            else:
                speak(result)
            
            # Clear input
            st.session_state.user_input = ""

# Quick access buttons
st.subheader("Quick Commands")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Time", key="quick_time"):
        speak(get_time())
with col2:
    if st.button("Date", key="quick_date"):
        speak(get_date())
with col3:
    if st.button("Weather", key="quick_weather"):
        speak(get_weather())
with col4:
    if st.button("Open Google", key="quick_google"):
        speak("Opening Google in a new tab")
        st.markdown("[Click here to open Google](https://www.google.com)", unsafe_allow_html=True)

# Display conversation history
st.markdown("<h3>Conversation History</h3>", unsafe_allow_html=True)
with st.container():
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f"<div class='response-area'><strong>Jarvis:</strong> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='user-message'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)

# Create greeting message at start
if not st.session_state.messages:
    # Determine greeting based on time
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    speak(f"{greeting} Jarvis at your service. How may I help you?")
