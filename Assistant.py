from AppOpener import open, close
import pyttsx3
import speech_recognition as sr

r = sr.Recognizer()
# Corrected: instantiate sr.Microphone
with sr.Microphone() as source:
    print("Say something")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

try:
    user_command = r.recognize_google(audio)
    print("What you said:", user_command)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
except Exception as e:
    print(f"An error occurred: {e}")
