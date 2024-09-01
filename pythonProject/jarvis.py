import pyttsx3
import speech_recognition as sr
import datetime
import requests
import os
import webbrowser
import smtplib
import random
import pyjokes

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to listen to user input
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        print("Sorry, I didn't catch that. Could you say that again?")
        speak("Sorry, I didn't catch that. Could you say that again?")
        return "None"
    return query.lower()


# Function to tell the current time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")


# Function to tell today's date and day
def tell_date_day():
    today = datetime.datetime.now().date()
    day = datetime.datetime.now().strftime("%A")
    speak(f"Today's date is {today} and it's {day}")


# Function to get weather info
def get_weather(city):
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_description = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature - 273.15:.2f} degrees Celsius with {weather_description}.")
    else:
        speak("City not found.")


# Function to open applications
def open_application(app_name):
    app_paths = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Update path if necessary
        # Add more applications and their paths here
    }

    app_path = app_paths.get(app_name.lower())
    if app_path:
        os.startfile(app_path)
        speak(f"Opening {app_name}")
    else:
        speak(f"Application {app_name} not found")


# Function to search on Google
def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Searching Google for {query}")


# Function to send an email
def send_email(to, subject, message):
    try:
        smtp_server = "smtp.gmail.com"  # Replace with your email provider's SMTP server
        smtp_port = 587
        from_email = "your_email@gmail.com"  # Replace with your email
        password = "your_password"  # Replace with your email password

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(from_email, to, email_message)
        server.quit()

        speak("Email has been sent successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I was unable to send the email.")


# Function to play music
def play_music():
    music_dir = "music"  # Replace with the path to your music folder
    songs = os.listdir(music_dir)
    if songs:
        os.startfile(os.path.join(music_dir, random.choice(songs)))
        speak("Playing music")
    else:
        speak("No music files found in the directory")


# Function to set a reminder
def set_reminder(reminder):
    with open("reminders.txt", "a") as file:
        file.write(f"{reminder}\n")
    speak(f"Reminder set for: {reminder}")


# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)


# Main loop to run JARVIS
if __name__ == '__main__':
    speak("Hello, I am JARVIS. How can I assist you today?")

    while True:
        query = take_command()

        if 'time' in query:
            tell_time()

        elif 'date' in query or 'day' in query:
            tell_date_day()

        elif 'weather' in query:
            speak("Which city's weather do you want to know?")
            city = take_command()
            get_weather(city)

        elif 'open' in query:
            app_name = query.replace('open ', '')
            open_application(app_name)

        elif 'search' in query:
            search_query = query.replace('search ', '')
            search_google(search_query)

        elif 'email' in query:
            speak("Who is the recipient?")
            recipient = take_command()
            speak("What is the subject?")
            subject = take_command()
            speak("What is the message?")
            message = take_command()
            send_email(recipient, subject, message)

        elif 'music' in query or 'play music' in query:
            play_music()

        elif 'set reminder' in query:
            speak("What should I remind you about?")
            reminder = take_command()
            set_reminder(reminder)

        elif 'joke' in query:
            tell_joke()

        elif 'exit' in query or 'stop' in query:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I can’t do that. Please ask something else.")
