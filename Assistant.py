from AppOpener import open, close
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
import os
import getpass

def speech_engine_settings():
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Assuming index 1 is the desired voice
    return engine

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
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

def main():
    load_dotenv()
    passkey = os.getenv('passkey')

    user_command = recognize_speech()
    if user_command:
        print("What you said:", user_command)
        
        if "lucy" in user_command:
            lucy = speech_engine_settings()
            lucy.say("Hello, my name is Lucy, please enter your passkey for authorization")
            lucy.runAndWait()
            
            auth_passkey = getpass.getpass("Enter your passkey: ")  
            if auth_passkey == passkey:
                lucy.say("Hello Niall, how may I assist you today?")
            else:
                lucy.say("You have entered an invalid passkey, Authorization failed")
            lucy.runAndWait()
        else:
            print("Error: 'lucy' not found in the command")
    else:
        print("Error: Could not process the command")

if __name__ == "__main__":
    main()
