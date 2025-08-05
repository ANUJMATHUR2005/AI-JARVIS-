🧠 Jarvis Voice Assistant with Virtual Environment:
📌 Overview:
This project is a Python-based voice assistant named Jarvis, designed to respond to voice commands and perform tasks like opening websites, 
fetching information, playing YouTube videos, scraping content from the web, and even responding to custom prompts using AI. 

The goal was to build a smart desktop assistant that responds naturally to your voice and can automate daily tasks.

The project was developed inside a Python virtual environment to keep dependencies isolated and the setup clean.
This makes it easier to share, run, and maintain without conflicts across different systems.

💡 How AI Helped Me :
This project was successfully built with the help of AI tools, especially ChatGPT, which provided step-by-step guidance, resolved code issues, explained complex logic, 
and helped integrate features like GPT-style responses using the g4f library (GPT for Free). 
AI truly acted as a co-pilot throughout the development process, making learning and building more efficient and enjoyable.

🛠️ Technologies & Libraries Used :
speech_recognition – for voice input
gtts and pyttsx3 – for converting text to speech
webbrowser, keyboard, os – for executing system tasks
pywhatkit – for playing YouTube videos and more
pygame – for audio playback
bs4 (BeautifulSoup) – for web scraping
langdetect – for language detection
g4f – GPT For Free: AI-based responses without API keys


⚙️ Setup Instructions :
1. Clone the Repository
   https://github.com/ANUJMATHUR2005/AI-JARVIS-/new/main?filename=README.md

2. Create a Virtual Environment
   python -m venv venv

3. Activate the Environment
   a. On Windows:
     venv\Scripts\activate
   b. On Mac/Linux:
     source venv/bin/activate
   
4. Install Required Packages
   pip install -r requirements.txt

5. Run the Assistant
   python main.py

📦 Managing Dependencies :
To generate a list of installed packages inside your virtual environment for sharing or deployment, run:
  pip freeze > requirements.txt

👤 Author :
Created by ANUJ MATHUR, a passionate Python learner and developer. Special thanks to AI (ChatGPT) for assisting in building, debugging, and enhancing this project 
from start to finish.

📝 License
This project is licensed under the MIT License, which means you're free to use, modify, and distribute it with proper credit.
