# 🎙️ Jarvis - Python Voice Assistant
Jarvis is a simple yet powerful Python-based desktop voice assistant that can perform tasks like telling the time, fetching weather, telling jokes, opening websites, announcing IP address, and even controlling your system (shutdown, restart, lock)!

# 🚀 Features

🎤 Voice Command Recognition (Speech-to-Text)

🔊 Text-to-Speech Responses

📅 Tells Current Time and Date

🌦️ Fetches Real-Time Weather for Bahawalpur (via OpenWeatherMap)

🤣 Tells Random Jokes

💬 Speaks Inspirational and Motivational Quotes

🌐 Opens Popular Websites (Google, YouTube, Facebook, etc.)

🖥️ System Controls (Shutdown, Restart, Lock)

🌍 Announces Public IP Address

🔇 Mute/Unmute Assistant Voice

🧠 Smart fallback for unrecognized commands


🛠️ Installation
Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/jarvis-voice-assistant.git
cd jarvis-voice-assistant
Install the required libraries

bash
Copy
Edit
pip install SpeechRecognition pyttsx3 pyaudio requests
Note: You may need to install PyAudio separately depending on your system. For Windows:

bash
Copy
Edit
pip install pipwin
pipwin install pyaudio
Set up OpenWeatherMap API Key

Sign up at OpenWeatherMap and get your API key.

Replace the api_key inside get_weather() function with your key.

🧑‍💻 How to Run
Simply run the script:

bash
Copy
Edit
python jarvis.py
Jarvis will greet you and start listening to your voice commands!

