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
import pywhatkit as kit
import random

load_dotenv()
api_key = os.getenv('gemini_api_key')
weather_api = os.getenv('open_weather_api')

# Configuration and initialization of the gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-pro")

# English language model for spaCy
nlp = spacy.load("en_core_web_sm")

health_tips = [
    "Drink at least 8 glasses of water to stay hydrated.",
    "Eat a balanced diet rich in fruits, vegetables, and whole grains.",
    "Get at least 7-8 hours of sleep each night.",
    "Practice deep breathing exercises to reduce stress.",
    "Take breaks and stretch regularly if you sit for long periods.",
    "Incorporate more physical activity into your daily routine."
]

fitness_tips = [
    "Aim for at least 30 minutes of moderate exercise, such as brisk walking, every day.",
    "Incorporate strength training exercises into your workout routine.",
    "Warm up before exercising and cool down afterward.",
    "Stay consistent with your workouts to see long-term benefits.",
    "Listen to your body and avoid overexertion.",
    "Try different types of exercise to keep your routine interesting."
]

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
        recognized_text = r.recognize_google(audio).lower()
        return recognized_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def health_tips_function(command):
    return f"Here are some fitness tips, {health_tips}"

def fitness_tips_function(command):
    return f"Here are some fitness tips, {fitness_tips}"

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
        "youtube": play_yt_content_function,
        "thank you": custom_responses_function,
        "how are you": custom_responses_function,
        "i am doing fine": custom_responses_function,
        "i am talking to someone else": custom_responses_function,
        "health tips:": health_tips_function,
        "fitness tips": fitness_tips_function,
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
    
    lucy.say("In how many minutes should I remind you?")
    lucy.runAndWait()
    interval_text = recognize_speech("Listening for time interval...")
    if interval_text is None:
        return "I couldn't understand the time interval. Please try again."

    try:
        # Attempt to extract minutes from the recognized text
        interval = int(next(filter(str.isdigit, interval_text), 0))
        set_reminder(interval*60, reminder_message)
        return f"Reminder set for {interval} minutes."
    except ValueError:
        return "I couldn't understand the time interval. Please try again."

def play_yt_content_function(command):
    yt_content = command.replace("play video", "").strip()
    kit.playonyt(yt_content)
    return f"Certainly"

def custom_responses_function(command):
    if "thank you" in command:
        return f"Your welcome"
    elif "how are you" or "how are you doing" in command:
        return f"i am doing well, thanks for asking, what about you?"
    elif "i am doing fine" in command or "i am fine" in command or "i'm good" in command:
        return f"That's good to hear"
    elif "i was talking to someone else" in command:
        return "i'm sorry for interrupting your conversation, please continue"
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
        temp_in_celcius = temperature-273.15
        final_temp_in_celcius = round(temp_in_celcius, 2)
        description = weather['description']
        return f"The weather in {city} is {description} with a temperature of {final_temp_in_celcius}°C."
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
                            elif result == "do not exit" or result == "don't exit":
                                continue
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
