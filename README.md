# Jarvis Voice Assistant - Streamlit App

A web-based version of the Jarvis Voice Assistant implemented using Streamlit. This application provides an interactive interface to check time, date, weather, and open various websites.

![Jarvis Assistant](https://via.placeholder.com/800x400?text=Jarvis+Voice+Assistant)

## Features

- 🕒 **Time & Date**: Get current time and date information
- 🌤️ **Weather Updates**: Check weather conditions for any city
- 🌐 **Website Navigation**: Quick access to popular websites
- 💬 **Chat Interface**: Interact with Jarvis through text commands
- 🎮 **Quick Command Buttons**: One-click access to common functions

## Demo

Access the live demo (if deployed): [Jarvis Assistant Demo](https://your-streamlit-app-url-here)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jarvis-streamlit.git
   cd jarvis-streamlit
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the app locally**
   ```bash
   streamlit run app.py
   ```

6. The app will open in your default web browser at `http://localhost:8501`

## Deployment

### Deploying to Streamlit Cloud

1. Push your code to a GitHub repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Sign in with your GitHub account
4. Deploy your app by connecting to your repository
5. Set up any required secrets (like API keys)

### Required Secrets

For the weather functionality, you need an OpenWeatherMap API key:

1. Get an API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Add it to your Streamlit secrets:
   - Locally: Create a `.streamlit/secrets.toml` file with:
     ```toml
     OPENWEATHER_API_KEY = "your_api_key_here"
     ```
   - On Streamlit Cloud: Add it in the app settings under "Secrets"

## Usage

### Available Commands

- **Time**: "What's the time?" or "Tell me the time"
- **Date**: "What's today's date?" or "Tell me the date"
- **Weather**: "What's the weather?" or "Check weather in [city name]"
- **Open Websites**: "Open Google", "Open YouTube", etc.
- **Exit**: "Goodbye", "Exit", or "Quit"

### Quick Command Buttons

Use the buttons at the top of the interface for one-click access to common functions:
- Time
- Date
- Weather
- Open Google

## Differences from Desktop Version

This Streamlit version differs from the original desktop application:

1. **Voice Input/Output**: Using text-based input instead of microphone
2. **System Commands**: Cannot perform system operations (shutdown, restart)
3. **Browser Integration**: Opens links in new tabs rather than default browser
4. **Security**: Runs in a web environment with appropriate restrictions

## Future Enhancements

- Add voice input functionality using Streamlit Components with JavaScript
- Implement text-to-speech for responses
- Add more API integrations (news, reminders, etc.)
- Create a mobile-responsive design
- Add user authentication

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original desktop Jarvis assistant code
- [Streamlit](https://streamlit.io/) for the web app framework
- [OpenWeatherMap](https://openweathermap.org/) for weather data

---

Created with ❤️ by [Your Name]
