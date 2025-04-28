import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import requests

# ====================== INITIALIZATION ======================
engine = pyttsx3.init()

# ====================== SPEECH FUNCTIONS ======================
def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def get_audio():
    """Capture and recognize speech with enhanced reliability"""
    r = sr.Recognizer()
    
    # Print available mics (debugging help)
    print("\nAvailable microphones:")
    for i, mic in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{i}: {mic}")
    
    # Use primary mic (change index if needed)
    with sr.Microphone(device_index=0) as source:
        # Dynamic energy threshold adjustment
        r.dynamic_energy_threshold = True
        r.pause_threshold = 1.5
        r.non_speaking_duration = 0.5
        
        print("\nListening... (Speak now)")
        r.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=10)
            print("Processing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"API Error: {e}")
            speak("I'm having trouble connecting to the internet")
            return None

# ====================== CORE FUNCTIONS ======================
def greet():
    """Personalized greeting based on time"""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        speak("Good morning sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir!")
    else:
        speak("Good evening sir!")
    speak("Jarvis at your service. How may I help you?")

def get_time():
    """Announce current time"""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")

def get_date():
    """Announce current date"""
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today is {current_date}")

# ====================== WEATHER FUNCTION ======================
def get_weather():
    """Fetch and announce weather information for Bahawalpur"""
    city = "Bahawalpur"
    api_key = '47f5042f9812fe43a495b8daaf14ab5e'  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] == "404":
        speak(f"City {city} not found.")
    else:
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]
        
        speak(f"The weather in {city} is {description}. The temperature is {temperature}°C with a pressure of {pressure} hPa and humidity of {humidity}%.")

# ====================== JOKES, QUOTES FUNCTIONS ======================
def tell_joke():
    """Tell a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why was the math book sad? Because it had too many problems.",
        "What do you call fake spaghetti? An impasta!",
        "Tell me the first ten digits of your sister phone number!",
        "Some Love one some love two. I love one that is you!."
    ]
    joke = random.choice(jokes)
    speak(joke)

def random_quote():
    """Say a random motivational quote"""
    quotes = [
        "Believe you can and you're halfway there.",
        "The only way to do great work is to love what you do.",
        "Dream big and dare to fail.",
        "Hardships often prepare ordinary people for an extraordinary destiny.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts."
    ]
    quote = random.choice(quotes)
    speak(quote)

def inspirational_quote():
    """Say a random inspirational quote"""
    inspirations = [
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Don't watch the clock; do what it does. Keep going.",
        "It always seems impossible until it's done.",
        "Success doesn’t just find you. You have to go out and get it."
    ]
    inspiration = random.choice(inspirations)
    speak(inspiration)


# ====================== IP Address ======================
def get_ip_address():
    """Get public IP"""
    try:
        ip = requests.get('https://api.ipify.org').text
        speak(f"Your public IP address is {ip}")
    except Exception as e:
        speak("Sorry, I couldn't fetch the IP address.")

# ====================== SYSTEM CONTROL FUNCTIONS ======================
def shutdown_system():
    """Shutdown the computer"""
    speak("Shutting down the system.")
    os.system("shutdown /s /f /t 1")  # For Windows

def restart_system():
    """Restart the computer"""
    speak("Restarting the system.")
    os.system("shutdown /r /f /t 1")  # For Windows

def lock_system():
    """Lock the computer"""
    speak("Locking the system.")
    os.system("rundll32.exe user32.dll,LockWorkStation")  # For Windows

# ====================== MUTE/UNMUTE FUNCTIONS ======================
def mute():
    """Mute the assistant"""
    global is_muted
    is_muted = True
    speak("I am now muted. I will not speak until unmuted.")

def unmute():
    """Unmute the assistant"""
    global is_muted
    is_muted = False
    speak("I am now unmuted. How can I assist you?")


# ====================== MAIN PROGRAM ======================
def main():
    greet()
    
    while True:
        query = get_audio()
        
        if not query:
            speak("I didn't catch that. Please try again.")
            continue
            
        # Time/Date Commands
        if 'time' in query:
            get_time()
        elif 'date' in query:
            get_date()

         # Jokes and Quotes
        elif 'tell a joke' in query:
            tell_joke()
        elif 'random quote' in query:
            random_quote()
        elif 'inspirational quote' in query or 'motivation' in query:
            inspirational_quote()

            
        # Weather Command (for Bahawalpur)
        elif 'weather' in query:
            get_weather()
        
        # Mute/Unmute Commands
        elif 'mute' in query:
            mute()
        elif 'unmute' in query:
            unmute()

        # IP ADDRESS
        elif 'what\'s my ip' in query or 'my ip address' in query:
            get_ip_address()
        
        # Website Commands (open with default browser)
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif 'open facebook' in query:
            speak("Opening Facebook")
            webbrowser.open("https://www.facebook.com")
        elif 'open instagram' in query:
            speak("Opening Instagram")
            webbrowser.open("https://www.instagram.com")
        elif 'open twitter' in query:
            speak("Opening Twitter")
            webbrowser.open("https://www.twitter.com")
        elif 'open email' in query:
            speak("Opening Gmail")
            webbrowser.open("https://mail.google.com")
        elif 'open linkedin' in query:
            speak("Opening LinkedIn")
            webbrowser.open("https://www.linkedin.com")
        elif 'open github' in query:
            speak("Opening GitHub")
            webbrowser.open("https://www.github.com")
        elif 'open chat' in query or 'open gpt' in query:
            speak("Opening ChatGPT")
            webbrowser.open("https://chat.openai.com")
        elif 'open microsoft edge' in query:
            speak("Opening Microsoft Edge")
            webbrowser.open("https://www.microsoft.com/edge")
        elif 'watch anime' in query:
            speak("Opening Aniwatch")
            webbrowser.open("https://aniwatch.to")
        elif 'open streamlit' in query:
            speak("Opening Streamlit")
            webbrowser.open("https://streamlit.io")
        elif 'generate images' in query:
            speak("Opening Ideogram")
            webbrowser.open("https://ideogram.ai")
    
        # System Control Commands
        elif 'shutdown' in query:
            shutdown_system()
        elif 'restart' in query:
            restart_system()
        elif 'lock system' in query:
            lock_system()
            
        # Exit Command
        elif 'exit' in query or 'quit' in query or 'bye' in query:
            speak("Shutting down. Have a nice day sir!")
            break
            
        # Fallback for unrecognized commands
        else:
            speak("I didn't understand that command. Please try again.")

if __name__ == "__main__":
    main()
