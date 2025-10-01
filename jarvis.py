import speech_recognition as sr
import webbrowser
import pyttsx3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# -----------------------------
# Gmail API Setup
# -----------------------------
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def read_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        speak("No new emails found.")
    else:
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            snippet = txt['snippet']
            speak(snippet)

# -----------------------------
# Voice + Speech Setup
# -----------------------------
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# Command Processing
# -----------------------------
def processcommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("http://google.com")    
    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("http://youtube.com")
    elif "open instagram" in c.lower():
        speak("Opening Instagram")
        webbrowser.open("http://instagram.com")
    elif "open spotify" in c.lower():
        speak("Opening Spotify")
        webbrowser.open("http://spotify.com")
    elif "read emails" in c.lower():
        speak("Fetching your latest emails")
        read_emails()
    else:
        speak("Sorry, I didn't understand the command.")

# -----------------------------
# Main Program
# -----------------------------
if __name__== "__main__":
    speak("Initializing Jarvis.....")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            word = recognizer.recognize_google(audio)
            print(f"You said: {word}")

            if "jarvis" in word.lower():   # Wake word
                speak("Yes")

                # Listen for the actual command
                with sr.Microphone() as source:
                    print("Jarvis Active... Listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                print(f"Command: {command}")
                processcommand(command)

        except Exception as e:
            print(f"Error: {e}")