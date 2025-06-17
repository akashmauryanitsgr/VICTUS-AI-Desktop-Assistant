import random
import sys
import traceback
import pyttsx3

# Initialize the TTS engine once
engine = None
def init_engine():
    global engine
    if engine is None:
        engine = pyttsx3.init()
        # Set voice to David
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'david' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                print(f"Using voice: {voice.name}")
                break
        # Set properties
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

def TTS(Text, func=lambda r=None: True):
    try:
        print("Starting TTS process...")
        init_engine()
        
        print("Speaking text...")
        engine.say(Text)
        engine.runAndWait()
        print("Speech completed")
        
        # Call the callback function when done
        if func:
            func(False)
            
        return True
    
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print("Stack trace:")
        traceback.print_exc()
        if func:
            func(False)
        return False

def TextToSpeech(Text, func=lambda r=None: True):
    try:
        if not Text or not isinstance(Text, str):
            print("Error: Invalid input text")
            return

        Data = str(Text).split(".")
        responses = ["The rest of the result has been printed to the chat screen, kindly check it out sir.","The rest of the text is now on the chat screen, sir, please check it.","You can see the rest of the text on the chat screen, sir.","The remaining part of the text is now on the chat screen, sir.","Sir, you'll find more text on the chat screen for you to see.","The rest of the answer is now on the chat screen, sir.","Sir, please look at the chat screen, the rest of the answer is there.","You'll find the complete answer on the chat screen, sir.","The next part of the text is on the chat screen, sir.","Sir, please check the chat screen for more information.","There's more text on the chat screen for you, sir.","Sir, take a look at the chat screen for additional text.","You'll find more to read on the chat screen, sir.","Sir, check the chat screen for the rest of the text.","The chat screen has the rest of the text, sir.","There's more to see on the chat screen, sir, please look.","Sir, the chat screen holds the continuation of the text.","You'll find the complete answer on the chat screen, kindly check it out sir.","Please review the chat screen for the rest of the text, sir.","Sir, look at the chat screen for the complete answer."]

        if len(Data) > 4 and len(Text) >= 250:
            TTS(" ".join(Text.split(".")[0:5]) + ". " + random.choice(responses), func)
        else:
            TTS(Text, func)
    except Exception as e:
        print(f"Error in TextToSpeech: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print("Stack trace:")
        traceback.print_exc()

if __name__ == "__main__":  
    try:
        while True:
            try:
                TextToSpeech(input("Enter the text : "))
            except KeyboardInterrupt:
                print("\nProgram terminated by user")
                sys.exit(0)
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
                continue
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

