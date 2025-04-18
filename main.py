import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception:
        print("Could not understand. Please repeat...")
        return None
    return query.lower()

def get_weather():
    api_key = "your_openweather_api_key"  # Replace with your OpenWeatherMap API Key
    city = "your_city"  # Replace with your city name
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
    else:
        speak("Couldn't retrieve weather info.")

if __name__ == "__main__":
    wish_me()
    while True:
        command = take_command()
        if command is None:
            continue
        elif "time" in command:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif "wikipedia" in command:
            speak("Searching Wikipedia...")
            result = wikipedia.summary(command.replace("wikipedia", ""), sentences=2)
            speak("According to Wikipedia")
            speak(result)
        elif "open google" in command:
            webbrowser.open("https://www.google.com")
        elif "weather" in command:
            get_weather()
        elif "stop" in command or "bye" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't catch that.")
