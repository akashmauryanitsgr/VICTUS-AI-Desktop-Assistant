import screen_brightness_control as sbc
from Backend.TextToSpeech import TextToSpeech

def control_brightness(task: str):
    try:
        task = task.lower()

        if 'increase' in task:
            current = sbc.get_brightness(display=0)[0]
            new_brightness = min(current + 20, 100)
            sbc.set_brightness(new_brightness)
            TextToSpeech(f"Brightness increased to {new_brightness} percent.")

        elif 'decrease' in task:
            current = sbc.get_brightness(display=0)[0]
            new_brightness = max(current - 20, 0)
            sbc.set_brightness(new_brightness)
            TextToSpeech(f"Brightness decreased to {new_brightness} percent.")

        elif 'set' in task:
            # Extract number from string
            import re
            match = re.search(r'\d{1,3}', task)
            if match:
                level = int(match.group())
                level = min(max(level, 0), 100)
                sbc.set_brightness(level)
                TextToSpeech(f"Brightness set to {level} percent.")
            else:
                TextToSpeech("Please provide a valid brightness level.")

        elif 'max' in task or 'full' in task:
            sbc.set_brightness(100)
            TextToSpeech("Brightness set to maximum.")

        elif 'min' in task or 'low' in task:
            sbc.set_brightness(0)
            TextToSpeech("Brightness set to minimum.")

        else:
            TextToSpeech("Sorry, I didn't understand the brightness command.")

    except Exception as e:
        TextToSpeech("There was an error adjusting brightness.")
        print(f"[ERROR] Brightness control failed: {e}")
