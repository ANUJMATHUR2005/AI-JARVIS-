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
import sys

conversation_history = []

# Recognizer and TTS Engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak_gtts(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
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
        speak_old("Answer is ready but audio playback failed.")

def speak(text):
    speak_gtts(text, lang='en')

# AI Chat with g4f
def ai_chat(prompt):
    global conversation_history

    try:
        lang = detect(prompt) if detect(prompt) in ['hi', 'en'] else 'en'
    except:
        lang = 'en'

    system_prompt = (
        "You are a helpful assistant that always replies in English."
        if lang == 'en' else
        "आप एक सहायक एआई हैं जो हमेशा हिंदी में उत्तर देते हैं।"
    )

    # Only add system prompt once, at the start
    if not conversation_history:
        conversation_history.append({"role": "system", "content": system_prompt})

    # Add user prompt to history
    conversation_history.append({"role": "user", "content": prompt})

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history
        )

        response_text = str(response).strip()
        print("🧠 GPT:", response_text)

        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": response_text})

        speak_gtts(response_text, lang)

    except Exception as e:
        print("⚠️ GPT Error:", e)
        speak_old("Sorry, I couldn't get an answer from AI." if lang == 'en' else "माफ़ कीजिए, उत्तर नहीं मिला।")


# News Modules
def India_news():
    speak("Fetching latest India news from Times of India.")
    url = "https://timesofindia.indiatimes.com/briefs/india"
    webbrowser.open(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    headlines = soup.find_all("h2")[2:7]
    if not headlines:
        speak("Sorry, couldn't find any India news headlines.")
        return
    for i, h in enumerate(headlines, start=1):
        news = h.get_text().strip()
        print(f"Headline {i}: {news}")
        speak(news)
    speak("And many more...")
    sys.exit()
        

def Rajasthan_news():
    speak("Fetching latest Rajasthan news from Times of India.")
    url = "https://timesofindia.indiatimes.com/india/rajasthan"
    webbrowser.open(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    headlines = soup.find_all("span", class_="w_tle")
    if not headlines:
        speak("Sorry, couldn't find any Rajasthan news headlines.")
        return
    for i, h in enumerate(headlines[:5], start=1):
        news = h.get_text().strip()
        print(f"Headline {i}: {news}")
        speak(news)
    speak("And many more...")
    sys.exit()

def Global_news():
    speak("Fetching latest Global news from Times of India.")
    url = "https://timesofindia.indiatimes.com/briefs"
    webbrowser.open(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    headlines = soup.find_all("h2")[2:7]
    if not headlines:
        speak("Sorry, couldn't find any Global news headlines.")
        return
    for i, h in enumerate(headlines, start=1):
        news = h.get_text().strip()
        print(f"Headline {i}: {news}")
        speak(news)
    speak("And many more...")
    sys.exit()

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


    if "reset chat" in c or "clear conversation" in c:
        conversation_history.clear()
        speak("conversation history cleared.")
        return
   

    if any(word in c for word in ["exit", "quit", "stop", "bye", "close jarvis", "shutdown"]):
        speak("Goodbye!")
        print("👋 Exiting Jarvis.")
        sys.exit()
 
    if "weather" in c or "temperature" in c:
        speak("Showing weather information for your location.")
        webbrowser.open("https://www.google.com/search?q=weather")
        sys.exit()

    if c.startswith("play "):
        command = c[5:].strip()
        song = command.split(" on ")[0].strip() if " on " in command else command
        if any(p in c for p in ["spotify", "brave", "google", "gaana", "saavan"]):
            speak("We can't play on that platform. Would you like to play it on YouTube?")
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("🎤 Listening for yes or no...")
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=4)
                user_response = recognizer.recognize_google(audio).lower()
                print(f"You said: {user_response}")
                
                if "no" in user_response:
                    speak("Okay, cancelling the command.")
                    sys.exit()
                elif "yes" in user_response:
                    speak(f"Playing {song} on YouTube.")
                    pywhatkit.playonyt(song)
                    sys.exit()
                    
                else:
                    speak("Invalid response.")
                    sys.exit()
            except Exception as e:
                print("Voice recognition failed:", e)
                speak("Sorry, something went wrong while listening.")
                sys.exit()
        else:
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)
            sys.exit()

    websites = {
        "google": "https://google.com",
        "facebook": "https://facebook.com",
        "youtube": "https://youtube.com",
        "linkedin": "https://linkedin.com",
        "spotify": "https://spotify.in"
    }

    for name, url in websites.items():
        if f"open {name}" in c or name in c:
            speak(f"Opening {name.capitalize()}")
            webbrowser.open(url)
            sys.exit()

    ai_chat(c)

# Main Loop
if __name__ == "__main__":
    print("Initializing Jarvis...")
    print("🎙️ Jarvis is ready.")
    speak("Hey, how can I help you?")

    while True:
        try:
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

                lower_command = command.lower()

                if "india news" in lower_command:
                    India_news()
                    break

                elif "rajasthan news" in lower_command:
                    Rajasthan_news()
                    break

                elif "global news" in lower_command:
                    Global_news()
                    break

                elif "news" in lower_command:
                    read_news()
                    break

                processCommand(command)

                
        except sr.UnknownValueError:
            print("Didn't catch that.")
            speak("I didn't catch that. Could you please repeat?")
        except sr.RequestError as e:
            print("Could not request results from Google:", e)
            speak("Sorry, I couldn't connect to the internet.")
        except Exception as e:
            print("Unexpected error:", e)
            speak("Something went wrong. Please try again.")
