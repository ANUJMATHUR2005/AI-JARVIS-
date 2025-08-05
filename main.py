import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import pygame
import os
import pywhatkit
from bs4 import BeautifulSoup
import keyboard
import g4f
from langdetect import detect

# Creates a recognizer object
recognizer = sr.Recognizer()    
# Initializes the text-to-speech engine.
engine = pyttsx3.init()

def speak_old(text):
    engine = pyttsx3.init() # Initializes a new TTS engine every time
    engine.setProperty('rate', 400)  # Sets the speech rate to 400 wpm (very fast)
    engine.say(text)  # Queues the text to be spoken
    engine.runAndWait()  # Processes the queued speech
 
def speak(text):
    tts = gTTS(text, lang='en', slow=False)  # Converts text to speech using Google TTS
    tts.save('temp.mp3')   # Saves audio as temporary mp3
    pygame.mixer.init() # Initializes the mixer (Which can loads, play the mp3/ audio)
    pygame.mixer.music.load('temp.mp3') # Loads the mp3 file
    pygame.mixer.music.play() # Plays the audio
    while pygame.mixer.music.get_busy():  # Waits for playback to finish
        pygame.time.Clock().tick(10) 
    pygame.mixer.quit() # Closes the mixer
    os.remove("temp.mp3") # Deletes the temporary mp3

#AI chat
def ai_chat(prompt):
    try:
        try:
            lang = detect(prompt)
            if lang not in ['hi', 'en']:
                lang = 'en'
        except:
            lang = 'en'

        system_prompt = (
            "You are a helpful assistant that always replies in English."
            if lang == 'en' else
            "आप एक सहायक एआई हैं जो हमेशा हिंदी में उत्तर देते हैं।"
        )

        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        response_text = str(response)
        print("🧠 GPT:", response_text)
        speak(response_text)

        try:
            tts = gTTS(response_text, lang=lang, slow=False)
            tts.save('temp.mp3')
            pygame.mixer.init()
            pygame.mixer.music.load('temp.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
            os.remove("temp.mp3")
        except Exception as e:
            print("🔊 TTS Error:", e)
            speak("Answer is ready but audio playback failed.")

    except Exception as e:
        print("⚠️ GPT Error:", e)
        speak("Sorry, I couldn't get an answer from AI." if lang == 'en' else "माफ़ कीजिए, उत्तर नहीं मिला।")
        exit()


def India_news():
    speak("Fetching latest India news from Times of India.")
    webbrowser.open("https://timesofindia.indiatimes.com/briefs/india")
    url = "https://timesofindia.indiatimes.com/briefs/india"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    headlines = soup.find_all("h2")[2:7]

    if not headlines:
        speak("Sorry, couldn't find any India news headlines.")
        return

    for i, h in enumerate(headlines, start=1):
        news = h.get_text().strip()
        print(f"Headline {i}: {news}")
        speak(f"Headline {i}: {news}")

def Rajasthan_news():
    speak("Fetching latest Rajasthan news from Times of India.")
    webbrowser.open("https://timesofindia.indiatimes.com/india/rajasthan")
    url = "https://timesofindia.indiatimes.com/india/rajasthan"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    headlines = soup.find_all("span", class_="w_tle")

    if not headlines:
        speak("Sorry, couldn't find any Rajasthan news headlines.")
        return

    for i, h in enumerate(headlines[:5], start=1):
        news = h.get_text().strip()
        print(f"Headline {i}: {news}")
        speak(f"Headline {i}: {news}")

def Global_news():
    speak("Fetching latest Global news from Times of India.")
    webbrowser.open("https://timesofindia.indiatimes.com/briefs")
    url = "https://timesofindia.indiatimes.com/briefs"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    headlines = soup.find_all("h2")[2:7]

    if not headlines:
        speak("Sorry, couldn't find any Global news headlines.")
        return

    for i, h in enumerate(headlines, start=1):
        news = h.get_text().strip()
        print(f"Headline {i}: {news}")
        speak(f"Headline {i}: {news}")

def read_news():
    try:
        speak("What would you like: India, Rajasthan, or Global news?")
        print("Listening for your choice...")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=3)
        word = recognizer.recognize_google(audio).lower()
        print(f"{word} news")

        if "global" in word:
            Global_news()
        elif "india" in word:
            India_news()
        elif "rajasthan" in word:
            Rajasthan_news()
        else:
            speak("Incorrect command. Please say India, Rajasthan, or Global.")

    except Exception as e:
        print("Error while fetching news:", e)
        speak("Sorry, I couldn't fetch the news right now.")

def processCommand(c):
    c = c.lower()

    exit_keywords = ["exit", "quit", "stop", "bye", "close jarvis", "shutdown"]
    if any(word in c for word in exit_keywords):
        speak("Goodbye!")
        print("👋 Exiting Jarvis.")
        exit()

    if "weather" in c or "temperature" in c:
        speak("Showing weather information for your location.")
        webbrowser.open("https://www.google.com/search?q=weather")
        return

    if "news" in c:
        read_news()
        return

    # Play Command
    unauthorized_platforms = ["spotify", "brave", "google", "gaana", "saavan"]

    if c.startswith("play "):
        lowered_c = c.lower()
        command = c[5:].strip()
        song = command.split(" on ")[0].strip() if " on " in command else command

        for platform in unauthorized_platforms:
            if platform in lowered_c:
                print(f"We can't play on {platform.capitalize()} as we only have authorization with YouTube!")
                speak(f"We can't play on {platform.capitalize()} as we only have authorization with YouTube!")

                print("Wanna go with YouTube?")
                speak("Would you like to play it on YouTube?")

                try:
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        print("🎤 Listening for yes or no...")
                        audio = recognizer.listen(source, timeout=6, phrase_time_limit=4)

                    try:
                        user_response = recognizer.recognize_google(audio).lower()
                        print(f"You said: {user_response}")

                        if "yes" in user_response:
                            if song:
                                speak(f"Playing {song} on YouTube.")
                                pywhatkit.playonyt(song)
                                exit()
                            else:
                                speak("I didn't catch the song name.")
                            return

                        elif "no" in user_response:
                            print("Okay, cancelling the command.")
                            speak("Okay, cancelling the command.")
                            return

                        else:
                            speak("Invalid response. Please try again.")
                            return

                    except sr.UnknownValueError:
                        print("Could not understand the response.")
                        speak("Sorry, I couldn't understand what you said.")
                        return

                except Exception as e:
                    print("Voice recognition failed:", e)
                    speak("Sorry, something went wrong while listening.")
                    return

        # Play directly on YouTube
        if song:
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)
        else:
            speak("I didn't catch the song name.")
        return

    # Open websites
    websites = {
        "google"  : "https://google.com",
        "facebook": "https://facebook.com",
        "youtube" : "https://youtube.com",
        "linkedin": "https://linkedin.com",
        "spotify" : "https://spotify.in"
    }

    for name, url in websites.items():
        if f"open {name}" in c or name in c:
            speak(f"Opening {name.capitalize()}")
            webbrowser.open(url)
            exit()

    # Fallback to AI
    ai_chat(c)

# Main Loop
if __name__ == "__main__":
    print("Initializing Jarvis...")
    print("🎙️ Jarvis is ready.")
    speak("Hey, how can I help you?")

    while True:
        try:
            # Text command via Enter key
            if keyboard.is_pressed("Enter"):
                typed = input("\n💬 Type your command: ")
                processCommand(typed)
                continue
        except:
            pass

        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
                command = recognizer.recognize_google(audio)
                print(f"🎙️ '{command}'")

                if "India news" in command:
                    India_news()
                elif "Rajasthan news" in command:
                    Rajasthan_news()
                elif "Global news" in command:
                    Global_news()


                processCommand(command)
                exit()

        except sr.UnknownValueError:
            print("🤔 Didn't catch that.")
            speak("I didn't catch that. Could you please repeat?")
        except sr.RequestError as e:
            print("🔌 Could not request results from Google:", e)
            speak("Sorry, I couldn't connect to the internet.")
        except Exception as e:
            print("⚠️ Unexpected error:", e)
            speak("Something went wrong. Please try again.")