//I have written just this code for Instagram integration in future.....
import requests
import time,subprocess
from SpeechToText import SpeechRecognition
from TextToSpeech import TextToSpeech

# Replace with your values
TextToSpeech("Enter Your Acces Token")
#ACCESS_TOKEN = "EAAT47G75fckBOy8LUGTNExvhjczQBwZA1DSE2PUYMjJZBTwcbojBmSRvMHVxdCR75d9DQukEBRzrpZAPuPZBPZBSpnLRFHaSAQVZArwXHTvOq9fRLTZBIIZAiDHLgz1rFBLEbfqtoklSwaEc7ZAJU5mLGPEgWu88p66f5uBlGwjSLuKSkpwxmLFDcMOLfgCt57QbIaZA03QuiQeW59NvPmBRLb7HxdzbgWj4kZD"
result = subprocess.run(
             ['python', r'C:\Jarvis\Jarvis\Frontend\Input.py', 'email'], 
             capture_output=True, 
             text=True)
ACCESS_TOKEN = result.stdout.strip()
#IG_ACCOUNT_ID = "1399594264657353"
TextToSpeech("Enter Your Instagram Account Id")
result = subprocess.run(
             ['python', r'C:\Jarvis\Jarvis\Frontend\Input.py', 'email'], 
             capture_output=True, 
             text=True)
IG_ACCOUNT_ID = result.stdout.strip()


def get_conversations():
    url = f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/conversations"
    params = {
        "fields": "participants,messages.limit(2){message}",
        "access_token": ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    print(response)
    if response.ok:
        return response.json().get("data", [])
    else:
        print("Error getting conversations:", response.text)
        return []

def send_reply(conversation_id, message):
    url = f"https://graph.facebook.com/v19.0/{conversation_id}/messages"
    data = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, data=data)
    return response.ok

def main():
    conversations = get_conversations()
    if not conversations:
        TextToSpeech("You have no recent Instagram messages.")
        return

    for convo in conversations:
        participants = convo.get("participants", {}).get("data", [])
        if not participants:
            continue

        # Get the other user (not yourself)
        sender = next((p for p in participants if not p["name"].startswith("Your Name")), participants[0])
        last_msg = convo["messages"]["data"][0]["message"]
        convo_id = convo["id"]

        TextToSpeech(f"You have a message from {sender['name']}: {last_msg}")
        TextToSpeech("Do you want to reply? Say yes or no.")

        reply_intent = SpeechRecognition()
        if reply_intent and "yes" in reply_intent:
            TextToSpeech(f"What would you like to reply to {sender['name']}?")
            reply_text = SpeechRecognition()
            if reply_text:
                if send_reply(convo_id, reply_text):
                    TextToSpeech("Reply sent successfully.")
                else:
                    TextToSpeech("Failed to send the reply.")
        else:
            TextToSpeech("Okay, moving to the next message.")
        time.sleep(1)

if __name__ == "__main__":
    main()
