from webbrowser import open as webopen

from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser,platform
import subprocess
import requests
import keyboard
import asyncio
import logging
import os
from typing import List, Optional, Generator, AsyncGenerator
import sqlite3,time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = "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"

# Constants
CLASSES = [
    "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf",
    "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO",
    "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt",
    "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize Groq client
client = Groq(api_key=GroqAPIKey) if GroqAPIKey else None

# System messages
messages = []
SystemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {os.environ.get('Username', 'Assistant')}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."
}]

def google_search(topic: str) -> bool:
    """Perform a Google search for the given topic."""
    try:
        search(topic)
        return True
    except Exception as e:
        logger.error(f"Error in Google search: {e}")
        return False

def content_writer(topic: str) -> bool:
    """Generate content using AI and save it to a file."""
    def open_notepad(file_path: str) -> None:
        """Open a file in the default text editor."""
        try:
            default_text_editor = 'notepad.exe'
            subprocess.Popen([default_text_editor, file_path])
        except Exception as e:
            logger.error(f"Error opening notepad: {e}")

    def content_writer_ai(prompt: str) -> str:
        """Generate content using Groq AI."""
        if not client:
            logger.error("Groq client not initialized")
            return "Error: Groq API key not configured"

        try:
            messages.append({"role": "user", "content": prompt})
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=SystemChatBot + messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=1,
                stream=True,
                stop=None
            )

            answer = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    answer += chunk.choices[0].delta.content

            answer = answer.replace("</s>", "")
            messages.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            logger.error(f"Error in content generation: {e}")
            return f"Error: {str(e)}"

    try:
        topic = topic.replace("Content ", "")
        content = content_writer_ai(topic)

        # Ensure Data directory exists
        os.makedirs("Data", exist_ok=True)
        
        file_path = os.path.join("Data", f"{topic.lower().replace(' ', '')}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        open_notepad(file_path)
        return True
    except Exception as e:
        logger.error(f"Error in content writer: {e}")
        return False

def youtube_search(topic: str) -> bool:
    """Search YouTube for the given topic."""
    try:
        url = f"https://www.youtube.com/results?search_query={topic}"
        webbrowser.open(url)
        return True
    except Exception as e:
        logger.error(f"Error in YouTube search: {e}")
        return False

def play_youtube(query: str) -> bool:
    """Play a YouTube video for the given query."""
    try:
        playonyt(query)
        return True
    except Exception as e:
        logger.error(f"Error playing YouTube video: {e}")
        return False
import AppOpener as appopener


def safe_open_app(app_name: str):
    try:
        result = appopener.open(app_name, match_closest=False)  # disable fuzzy matching
        if not result:
            print(f"[ERROR] '{app_name}' not found or not installed.")
            return False
        else:
            print(f"[INFO] Attempted to open '{app_name}'.")
            return True
    except Exception as e:
        print(f"[EXCEPTION] Failed to open '{app_name}': {e}")


def open_app(app: str, session: requests.Session = requests.Session()) -> bool:
    """Open an application or its website."""
    b = safe_open_app(app)
    if(b == True):
        return

    try:
        # Common website mappings
        website_mappings = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'facebook': 'https://facebook.com',
            'twitter': 'https://twitter.com',
            'instagram': 'https://instagram.com',
            'linkedin': 'https://linkedin.com',
            'github': 'https://github.com',
            'gmail': 'https://gmail.com',
            'outlook': 'https://outlook.com',
            'amazon': 'https://amazon.com',
            'netflix': 'https://netflix.com',
            'spotify': 'https://spotify.com',
            'discord': 'https://discord.com',
            'reddit': 'https://reddit.com',
            'whatsapp': 'https://web.whatsapp.com',
            'telegram': 'https://web.telegram.org',
            'zoom': 'https://zoom.us',
            'slack': 'https://slack.com',
            'microsoft': 'https://microsoft.com',
            'apple': 'https://apple.com',
            'adobe': 'https://adobe.com',
            'dropbox': 'https://dropbox.com',
            'drive': 'https://drive.google.com',
            'docs': 'https://docs.google.com',
            'sheets': 'https://sheets.google.com',
            'slides': 'https://slides.google.com',
            'calendar': 'https://calendar.google.com',
            'maps': 'https://maps.google.com',
            'translate': 'https://translate.google.com',
            'photos': 'https://photos.google.com',
            'meet': 'https://meet.google.com',
            'classroom': 'https://classroom.google.com',
            'chat': 'https://chat.google.com',
            'keep': 'https://keep.google.com',
            'tasks': 'https://tasks.google.com',
            'sites': 'https://sites.google.com',
            'forms': 'https://forms.google.com',
            'jamboard': 'https://jamboard.google.com',
            'earth': 'https://earth.google.com',
            'news': 'https://news.google.com',
            'books': 'https://books.google.com',
            'scholar': 'https://scholar.google.com',
            'patents': 'https://patents.google.com',
            'finance': 'https://finance.google.com',
            'flights': 'https://flights.google.com',
            'hotels': 'https://hotels.google.com',
            'shopping': 'https://shopping.google.com',
            'express': 'https://express.google.com',
            'play': 'https://play.google.com',
            'movies': 'https://play.google.com/movies',
            'music': 'https://play.google.com/music',
            'books': 'https://play.google.com/books',
            'games': 'https://play.google.com/games',
            'apps': 'https://play.google.com/apps',
            'tv': 'https://play.google.com/tv',
            'newsstand': 'https://play.google.com/newsstand',
            'kiosk': 'https://play.google.com/kiosk',
            'devices': 'https://play.google.com/devices',
            'movies': 'https://play.google.com/movies',
            'music': 'https://play.google.com/music',
            'books': 'https://play.google.com/books',
            'games': 'https://play.google.com/games',
            'apps': 'https://play.google.com/apps',
            'tv': 'https://play.google.com/tv',
            'newsstand': 'https://play.google.com/newsstand',
            'kiosk': 'https://play.google.com/kiosk',
            'devices': 'https://play.google.com/devices'
        }

        # Check if the app name matches any known website
        app_lower = app.lower()
        for key, url in website_mappings.items():
            if key in app_lower:
                webbrowser.open(url)
                return True

        # If no direct match, try to construct a URL
        if not app.startswith(('http://www.', 'https://www.')):
            # Try common domain extensions
            for ext in ['.com', '.org', '.net', '.io', '.co']:
                try:
                    url = f"https://{app}{ext}"
                    webbrowser.open(url)
                    return True
                except:
                    continue

        # If all else fails, do a Google search
        search_query = f"open {app}"
        search(search_query)
        return True

    except Exception as e:
        logger.error(f"Error opening app/website: {e}")

        return False


def shutdown():
    system_platform = platform.system()
    os.system("shutdown /s /t 0")

def restart_pc():
    system = platform.system()
    if system == "Windows":
        print("yahan tak aa gya hai")
        os.system("shutdown /r /t 0")
        


def close_app(app: str) -> bool:
    """Close an application."""
    try:
        # For websites, we can't really "close" them, so just return True
        return True
    except Exception as e:
        logger.error(f"Error closing app: {e}")
        return False


def system_control(command: str) -> bool:
    """Control system functions like volume and mute."""
    try:
        if command == "mute":
            keyboard.press_and_release("volume mute")
        elif command == "unmute":
            keyboard.press_and_release("volume mute")
        elif command == "volume up":
            keyboard.press_and_release("volume up")
        elif command == "volume down":
            keyboard.press_and_release("volume down")
        return True
    except Exception as e:
        logger.error(f"Error in system control: {e}")
        return False
from Backend.TextToSpeech import TextToSpeech
async def translate_and_execute(commands: List[str]) -> AsyncGenerator[bool, None]:
    """Translate and execute a list of commands."""
    funcs = []
    #funcs = ["exit", "general", "realtime", "open", "close", "play", "generate image", "system", "content", "google search", "youtube search", "reminder", "whatsapp message", "whatsapp voice call", "whatsapp video call"]
    print(commands)
    for command in commands:
        
                
        if command.startswith("open "):
            if "open it" not in command and "open file" != command:
                funcs.append(asyncio.to_thread(open_app, command.removeprefix("open ")))
        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(close_app, command.removeprefix("close ")))
        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(play_youtube, command.removeprefix("play ")))
        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(content_writer, command.removeprefix("content ")))
        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(google_search, command.removeprefix("google search ")))
        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(youtube_search, command.removeprefix("youtube search ")))
        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(system_control, command.removeprefix("system ")))
        
        elif command.startswith("whatsapp message "):
            print( command.removeprefix("whatsapp message "))  
                  
            
            from Backend.WhatsApp import whatsapp_action
            #whatsapp_action("jyoti","message")
            query = command.removeprefix("whatsapp message ")
            whatsapp_action(query,"message")
            #funcs.append(asyncio.to_thread(whatsapp_action,"jyoti", 'message'))
        elif command.startswith("whatsapp voice call "):
            from Backend.WhatsApp import whatsapp_action
            query = command.removeprefix("whatsapp voice call ")
            whatsapp_action(query,"call")
            #funcs.append(asyncio.to_thread(whatsapp_action,command.removeprefix("whatsapp voice call "), 'call'))

        elif command.startswith("whatsapp video call "):
            from Backend.WhatsApp import whatsapp_action
            query = command.removeprefix("whatsapp video call")
            whatsapp_action(query,"video call")
            #funcs.append(asyncio.to_thread(whatsapp_action, command.removeprefix("whatsapp video call "), 'video'))
        
        elif command.startswith("brightness "):
            from Backend.Brightness import control_brightness            
            funcs.append(asyncio.to_thread(control_brightness, command.removeprefix("brightness ")))

        elif command.startswith("send email"):                     
            from Backend.EmailAutomation import send_email
            #from Frontend.GUI import ChatSection
            #chat_section = ChatSection()
            funcs.append(asyncio.to_thread(send_email, command.removeprefix("send email ")))

        elif command.startswith("read email"):                       
            from Backend.EmailAutomation import read_email
            funcs.append(asyncio.to_thread(read_email, command.removeprefix("read email ")))

        elif command.startswith("system shutdown "):            
            funcs.append(asyncio.to_thread(shutdown()))

        elif command.startswith("system restart "): 
            print("yahan tak a gye")           
            funcs.append(asyncio.to_thread(restart_pc()))

        elif command.startswith("register user"): 
            subprocess.run(['python', r'C:\Jarvis\Jarvis\Backend\RegisterFace.py'])


        else:
            logger.warning(f"No function found for command: {command}")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands: List[str]) -> bool:
    """Main automation function to execute commands."""
    try:
        async for _ in translate_and_execute(commands):
            pass
        return True
    except Exception as e:
        logger.error(f"Error in automation: {e}")
        return False 
