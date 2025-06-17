from groq import Groq
from googlesearch import search
from json import load, dump
from dotenv import dotenv_values
import os
import datetime

# Setup and load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")
GroqAPIKey = env_vars.get("GROQ_API_KEY")

client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar. ***
*** Just answer the question from the provided data in a professional way. ***"""

# Set up data directory and file paths
data_dir = os.path.join(os.getcwd(), "Data")
os.makedirs(data_dir, exist_ok=True)
chatlog_path = os.path.join(data_dir, "ChatLog.json")

# Ensure chat log file exists
if not os.path.exists(chatlog_path):
    with open(chatlog_path, "w") as f:
        dump([], f)

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    answer = f"The search results for '{query}' are:\n[start]\n"
    for result in results:
        answer += f"Title : {result.title}\nDescription : {result.description}\n\n"
    answer += "[end]"
    return answer

def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

def Information():
    now = datetime.datetime.now()
    return (
        "Use This Realtime Information if needed.\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours :{now.strftime('%M')} minutes :{now.strftime('%S')} seconds.\n"
    )

def RealtimeSearchEngine(prompt):
    global SystemChatBot

    with open(chatlog_path, "r") as f:
        messages = load(f)

    messages.append({"role": "user", "content": prompt})
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content

    answer = answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": answer})

    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))





'''from groq import Groq
from googlesearch import search
from json import load,dump
from dotenv import dotenv_values
import datetime

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GROQ_API_KEY")
client = Groq( api_key = GroqAPIKey )

System = f"""Hello, I am {Username}, You are a very accurate and advance AI chatbot named {Assistantname} which have realtime up-to-date information of internet.
*** Provide Answers In a Professional Way, make sure to add fullstops, comma, question mark and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

try:
    with open(r"Data\ChatLog.json","r") as f:
        messages = load(f)

except:
    with open(r"Data\ChatLog.json","w") as f:
        dump([],f)

def GoogleSearch(query):

    results = list(search(query, advanced=True, num_results=5))
    Answer =f"The search results for f'{query} 'are : \n[start]\n"

    for i in results:
        Answer += f"Title : {i.title}\nDiscription : {i.description}\n\n"

    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):

    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

""" Setting the variables, which will be used in the automation. """

SystemChatBot = [
    {"role": "system",
    "content": System},
    {"role": "user",
    "content": "Hi"},
    {"role": "assistant",
    "content": "Hello, how can I help you?"}]

def Information():

    data=""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data+=f"Use This Realtime Information. if needed\n"
    data+=f"Day: {day}\n"
    data+=f"Date: {date}\n"
    data+=f"Month: {month}\n"
    data+=f"Year: {year}\n"
    data+=f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data
    
def RealtimeSearchEngine(prompt):

    global SystemChatBot, messages

    with open(r"Data\ChatLog.json","r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})
    
    completion = client.chat.completions.create(
    model = "llama3-70b-8192",
    messages = SystemChatBot + [{"role": "system", "content": Information()}] + messages,
    temperature = 0.7,
    max_tokens = 2048,
    top_p = 1,
    stream = True,
    stop = None)

    Answer = ""
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    
    Answer = Answer.strip().replace("</s>","")
    messages.append({"role": "assistant", "content": Answer})

    with open(r"Data\ChatLog.json","w") as f:
        dump(messages,f,indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":

    while True:

        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))

'''