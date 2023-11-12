import time
import speech_recognition as sr
import os
import webbrowser
import openai
from gtts import gTTS
from io import BytesIO
import base64
import pygame
from config import apikey
import datetime

chatStr = ""

def chat(query):
    global chatStr
    print(f"Kaptan Kadir: {query}")

    openai.api_key = "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"
    chatStr += f"Kaptan Kadir: {query}\nAsu: "

    response = None
    while response is None:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=chatStr,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            message = response["choices"][0]["text"]
        except openai.error.RateLimitError as e:
            wait_time = int(e.headers.get("Retry-After",5))
            print("Rate limit reached. Waiting {wait_time} seconds.")
            time.sleep(2)

    response_text = response["choices"][0]["text"]
    say(response_text)
    chatStr += f"{response_text}\n"
    print(f"Asu: {response_text}")
    return response_text

def ai(prompt):
    openai.api_key = apikey
    text = f"DeepAI response for prompt: {prompt} \n*************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
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

def say(text):
    tts = gTTS(text=text, lang='tr')
    fp = BytesIO()
    tts.write_to_fp(fp)

    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="tr-TR")
            print(f"Kaptan Kadir: {text}")
        except sr.UnknownValueError:
            print("Ses anlaşılmadı.")
            text = ""
        except sr.RequestError:
            print("Çevrimiçi olarak ses tanıma hizmetine erişilemedi.")
            text = ""
        return text

if __name__ == '__main__':
    print('Welcome to Asu')
    say("Merhaba Kaptan Kadir")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"{site[0]} açılıyor...")
                webbrowser.open(site[1])

        if "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")
        if "valorant açar mısın" in query:
            os.startfile("C:/Riot Games/Riot Client/RiotClientServices.exe")
            say("Valorant açılıyor.")
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Saat {hour} ve {min} dakika.")
        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")
        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "Buradan Çık".lower() in query.lower():
            exit()
        elif "reset chat".lower() in query.lower():
            chatStr = ""
        else:
            print("Chatting...")
            chat(query)