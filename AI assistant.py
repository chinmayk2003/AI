import speech_recognition as sr
import os
import webbrowser
import openai
import pyttsx3
import datetime
import random
import pywhatkit

apikey =  # ""

chatStr = ""

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Sir: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Welcome, how can I assist you?")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        if "open music" in query:
            musicPath = r"C:\Users\chinm\Music\He's a Pirate (From Pirates of the Caribbean_ Dead Men Tell No TalesHans Zimmer vs D....mp3"
            os.startfile(musicPath)
        elif "what is the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} and {min} minutes")

        elif "open pass" in query.lower():
            os.startfile(r"C:\Program Files\Passky\Passky.exe")
        elif "search" in query.lower():
            search_query = query.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            say(f"searching{search_query}")
        elif "play" in query.lower():
            say("This is what I found for your search!")
            query = query.replace("youtube search", "")
            query = query.replace("youtube", "")
            query = query.replace("jarvis", "")
            web = "https://www.youtube.com/results?search_query=" + query
            webbrowser.open(web)
            pywhatkit.playonyt(query)
            say(f"Playing{query}")
        elif "Using artificial intelligence" in query:
            ai(prompt=query)
        elif "talk to AI" in query.lower():
            ai_response = ai(prompt="Let's chat about something interesting.")
            print("AI: ", ai_response)
            say(ai_response)
        elif "Jarvis Quit" in query.lower():
            exit()
        elif "reset chat" in query.lower():
            chatStr = ""
        else:
            print("Chatting...")
            chat(query)
