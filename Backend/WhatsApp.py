import sqlite3
import pyautogui
import subprocess,time

ASSISTANT_NAME = "victus"


con =sqlite3.connect(r"C:\Jarvis\Jarvis\jarvis.db")

cursor = con.cursor()

import unicodedata

def clean_query(query):
    # Normalize unicode, strip invisible characters
    query = unicodedata.normalize('NFKC', query)
    query = query.strip().lower()
    return query

def findContact(query):
    try:
        
        #query = query.strip().lower()
        query = clean_query(query)
        print(f"[DEBUG] Cleaned query: '{query}'")
        print(f"[DEBUG] Processed query: {query}")
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
          
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str
            print(mobile_number_str)
        return mobile_number_str
    except:
        print("not exist in contacts")
        return 0
    
from Backend.TextToSpeech import TextToSpeech

from Backend.SpeechToText import SpeechRecognition   
def whatsapp_action(contact, flag):
    
    print(type(contact))
    mobile_no = findContact(contact)
    
    name = contact
    if mobile_no == 0:
        TextToSpeech("Contact not found.")
        return
    
    if flag == 'message':
        target_tab = 12
        TextToSpeech("What message to send")       
        message = SpeechRecognition()
        time.sleep(4)
        print(message)
        
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 6
        message = ' '
        jarvis_message = "calling to "+name

    else:
        target_tab = 5
        message = ''
        jarvis_message = "staring video call with "+name

    
    # Encode the message for URL
    #encoded_message = quote(message)
    #print(encoded_message)
    # Construct the URL
    print(mobile_no)
    subprocess.run(f'start whatsapp://',shell=True)

    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={message}"

    # Construct the full command
    print(whatsapp_url)
    full_command = f'start "" "{whatsapp_url}"'
    
    # Open WhatsApp with the constructed URL using cmd.exe
    time.sleep(2)
    subprocess.run(full_command, shell=True)
    time.sleep(8)
    #subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(3)
    for i in range(1, target_tab+1):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    TextToSpeech(jarvis_message)
    
#whatsapp_action("Anubhav","message")