from AppOpener import open, close
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
import os
load_dotenv()
passkey = os.getenv('passkey')

r = sr.Recognizer()
# Corrected: instantiate sr.Microphone
with sr.Microphone() as source:
    print("Listening...")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
try:
    user_command = r.recognize_google(audio).lower()
    print("What you said:", user_command)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
except Exception as e:
    print(f"An error occurred: {e}")

if "lucy" in user_command:
    lucy = pyttsx3.init()
    rate = lucy.getProperty('rate')
    lucy.setProperty('rate', 130)
    voices = lucy.getProperty('voices')
    lucy.setProperty('voice', voices[1].id)
    lucy.say("Hello, my name is Lucy, please enter your passkey for authorization")
    lucy.runAndWait()
    lucy.stop()
    auth_passkey = input("Enter your passkey:")
    if auth_passkey == passkey:
        lucy = pyttsx3.init()
        rate = lucy.getProperty('rate')
        lucy.setProperty('rate', 130)
        voices = lucy.getProperty('voices')
        lucy.setProperty('voice', voices[1].id)
        lucy.say("Hello Niall, how may i assist you today?")
        lucy.runAndWait()
        lucy.stop()
    else:
        lucy = pyttsx3.init()
        rate = lucy.getProperty('rate')
        lucy.setProperty('rate', 130)
        voices = lucy.getProperty('voices')
        lucy.setProperty('voice', voices[1].id)
        lucy.say("You have entered an invalid passkey, Authorization failed")
        lucy.runAndWait()
        lucy.stop()

else:
    print("Error")