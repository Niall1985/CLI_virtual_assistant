import google.generativeai as genai
from dotenv import load_dotenv
import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import spacy
from datetime import datetime, timedelta
import threading
import getpass
import time
from AppOpener import open, close
from plyer import notification  
import requests
#import pywhatkit
load_dotenv()
api_key = os.getenv('gemini_api_key')
weather_api = os.getenv('open_weather_api')

# Configuration and initialization of the gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-pro")

# English language model for spaCy
nlp = spacy.load("en_core_web_sm")

def speech_engine_settings():
    lucy = pyttsx3.init()
    lucy.setProperty('rate', 130)
    voices = lucy.getProperty('voices')
    lucy.setProperty('voice', voices[1].id)
    return lucy

def set_reminder(interval, message):
    def reminder():
        time.sleep(interval)
        notification_title = "Reminder"
        notification_message = message
        notification.notify(title=notification_title, message=notification_message, timeout=10)

    reminder_thread = threading.Thread(target=reminder)
    reminder_thread.start()

def get_current_date_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    current_day = now.strftime("%A")
    return f"The current date is {current_date}, it is a {current_day} and the time is {current_time}"


def remind_drinking_water():
    def send_notification():
        while True:
            notification.notify(
                title="Reminder",
                message="This is your reminder to drink water",
                timeout=5
            )
            time.sleep(1800) 

    reminder_thread = threading.Thread(target=send_notification)
    reminder_thread.daemon = True
    reminder_thread.start()

def recognize_speech(prompt="Listening..."):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        return r.recognize_google(audio).lower()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def extract_city(command):
    doc = nlp(command)
    for ent in doc.ents:
        if ent.label_ == "GPE": 
            return ent.text
    return None

def execute_command(command):
    keywords = {
        "reminder": set_reminder_function,
        "date": get_current_date_time_function,
        "time": get_current_date_time_function,
        "open": open_application_function,
        "close": close_application_function,
        "google": google_search_function,
        "ask gemini to": gemini_function,
        "weather": weather_function,
        "open a file": open_file_function,
        "close a file": close_file_function,
        "delete a file": delete_file_function,
        "exit": exit_function
    }
    
    for keyword, function in keywords.items():
        if keyword in command:
            return function(command)
    return "I'm sorry, I didn't understand that command."

def set_reminder_function(command):
    lucy = speech_engine_settings()
    lucy.say("What is the reminder message?")
    lucy.runAndWait()
    reminder_message = recognize_speech("Listening for reminder message...")
    if reminder_message is None:
        return "I couldn't understand the reminder message. Please try again."
    
    lucy.say("In how many seconds should I remind you?")
    lucy.runAndWait()
    interval = recognize_speech("Listening for time interval...")
    if interval is None:
        return "I couldn't understand the time interval. Please try again."

    try:
        interval = int(interval)
        set_reminder(interval, reminder_message)
        return f"Reminder set for {interval} seconds."
    except ValueError:
        return "I couldn't understand the time interval. Please try again."



def get_current_date_time_function(command):
    return get_current_date_time()

def open_application_function(command):
    application_name = command.replace("open", "").strip()
    try:
        open(application_name)
        return f"Opening {application_name}."
    except Exception as e:
        return f"Could not open {application_name}. Error: {e}"
    
def close_application_function(command):
    application_name = command.replace("close", "").strip()
    try:
        close(application_name)
        return f"Closing {application_name}."
    except Exception as e:
        return f"Could not close {application_name}. Error: {e}"

def google_search_function(command):
    search_query = command.replace("google", "").strip()
    google_search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    webbrowser.open(google_search_url)
    return f"Opening Google search for: {search_query}"

def gemini_function(command):
    user = command.replace("ask gemini to", "").strip()
    response = model.generate_content(user)
    formatted_response = response.strip("*", "")
    print("Gemini Response:", formatted_response.text)  
    return formatted_response.text

def get_weather(city):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}"
    response = requests.get(weather_url)
    data = response.json()
    if data['cod'] == 200:
        main = data['main']
        weather = data['weather'][0]
        temperature = main['temp']
        temp_in_celcuis = temperature-273.15
        description = weather['description']
        return f"The weather in {city} is {description} with a temperature of {temp_in_celcuis}°C."
    else:
        return "City not found."

def weather_function(command):
    city = extract_city(command)
    print(city)
    if city:
        return get_weather(city)
    else:
        return "I couldn't determine the city for the weather request."

def open_file_function(command):
    lucy = speech_engine_settings()
    lucy.say("Please enter the file path you want to open:")
    lucy.runAndWait()
    file_path = input("Enter the file path: ").strip()
    try:
        if os.path.isfile(file_path):
            os.startfile(file_path)
            return f"Opening file: {file_path}"
        else:
            return f"File not found: {file_path}"
    except Exception as e:
        return f"Could not open file. Error: {e}"

def close_file_function(command):
    lucy = speech_engine_settings()
    lucy.say("Please enter the file path you want to close:")
    lucy.runAndWait()
    file_path = input("Enter the file path: ").strip()
    try:
        if os.path.isfile(file_path):
            os.close(file_path)
            return f"Closing file: {file_path}"
        else:
            return f"File not found: {file_path}"
    except Exception as e:
        return f"Could not close file. Error: {e}"

def delete_file_function(command):
    lucy = speech_engine_settings()
    lucy.say("Please enter the file path you want to delete:")
    lucy.runAndWait()
    file_path = input("Enter the file path: ").strip()
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            return f"Deleting file: {file_path}"
        else:
            return f"File not found: {file_path}"
    except Exception as e:
        return f"Could not delete file. Error: {e}"


def exit_function(command):
    return "exit"

def main():
    remind_drinking_water()
    while True:
        user_command = recognize_speech("Listening...")

        if user_command:
            print("What you said:", user_command)
            
            if "lucy" in user_command:
                lucy = speech_engine_settings()
                lucy.say("Hello, my name is Lucy, please enter your passkey for authorization")
                lucy.runAndWait()
                
                auth_passkey = getpass.getpass("Enter your passkey: ")
                if auth_passkey == os.getenv('passkey'):
                    lucy.say("Authorization successful, Hello Niall, how may I assist you today?")
                    lucy.runAndWait()
                    
                    while True:
                        lucy.say("Please tell me what you want me to do. To exit the program say 'exit'.")
                        lucy.runAndWait()
                        command = recognize_speech("Listening for command...")
                        if command:
                            result = execute_command(command)
                            if result == "exit":
                                lucy.say("Exiting the program. Goodbye Niall.")
                                lucy.runAndWait()
                                return
                            else:
                                lucy.say(result)
                                lucy.runAndWait()
                        else:
                            lucy.say("I didn't catch that. Could you please repeat?")
                            lucy.runAndWait()
                else:
                    lucy.say("You have entered an invalid passkey, Authorization failed.")
                    lucy.runAndWait()
            else:
                print("Error: 'lucy' not found in the command")
        else:
            print("Error: Could not process the command")

if __name__ == "__main__":
    main()
