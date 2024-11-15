import pyttsx3
import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import scrolledtext
import requests
import pyjokes
from datetime import datetime
import webbrowser
import wikipedia
from newsapi import NewsApiClient
import random
import json
import os
from tkinter import messagebox
import re
from speak import speak

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Virtual Assistant")
root.geometry("500x600")

# Create a scrolled text box for results
frame = tk.Frame(root)
frame.pack(pady=10)

result_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
result_box.grid(row=0, column=0, padx=5, pady=5)

command_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=5, font=("Arial", 12), bg="#f0f0f0")
command_box.grid(row=1, column=0, padx=5, pady=5)

status_label = tk.Label(root, text="Ready to assist!", font=("Arial", 12), fg="green")
status_label.pack(pady=5)

# Initialize pyttsx3
engine = pyttsx3.init()

def speak(text):
    def speak_thread():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=speak_thread).start()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            status_label.config(text="Command recognized!")
            command_box.insert(tk.END, "You said: " + command + "\n")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            status_label.config(text="Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            speak("Sorry, the service is down. Please try again later.")
            status_label.config(text="Service is down.")
            return None

def get_weather(location):
    api_key = "63d033c6d2ff634bff145bd6ec0b473a"
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    try:
        # Make the API request
        response = requests.get(base_url, params={
            "q": location,
            "appid": api_key,
            "units": "metric"
        })

        if response.status_code == 200:
            data = response.json()
            city = data.get("name")
            country = data["sys"].get("country")
            temperature = data["main"].get("temp")
            description = data["weather"][0].get("description")

            weather_info = (
                f"The current weather in {city}, {country} is {temperature}°C "
                f"with {description}."
            )
            print(weather_info)  # For debugging purposes
            speak(weather_info)
        elif response.status_code == 404:
            speak("Sorry, I couldn't find weather data for that location.")
        else:
            speak("Sorry, there was an error retrieving the weather data.")

    except Exception as e:
        print(f"Error: {e}")  # For debugging purposes
        speak("Sorry, there was an error connecting to the weather service.")

def tell_joke():
    try:
        joke = pyjokes.get_joke()
        speak(joke)
        display_input_output(f"Bot: {joke}")
        result_box.insert(tk.END, joke + "\n")
    except Exception as e:
        disoplay_input_output(f"Bot: Sorry, I couldn't fetch a joke right now. {str(e)}")    


def calculate(expression):
    try:
        # Use eval for simple math; ensure safety for input sanitization
        sanitized_expression = re.sub(r'[^\d\+\-\*/\(\)\.]', '', expression)
        result = eval(sanitized_expression)
        print(f"The result is {result}.")
        speak(f"The result is {result}.")
    except Exception as e:
        print("Error calculating.", str(e))
        speak("I couldn't calculate that.") 

def get_news():
    try:
        api = NewsApiClient(api_key='YOUR_NEWSAPI_KEY')  # Replace with your API key
        headlines = api.get_top_headlines(language='en')
        articles = headlines['articles'][:5]
        news = "Here are the top 5 news headlines:\n"
        for idx, article in enumerate(articles, start=1):
            news += f"{idx}. {article['title']}\n"
        speak(news)
        result_box.insert(tk.END, news + "\n")
    except Exception:
        speak("Sorry, I couldn't fetch the news right now.")

def get_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        fact = response.json().get("text", "Sorry, I couldn't fetch a fact right now.")
        speak(fact)
        result_box.insert(tk.END, fact + "\n")
    except Exception:
        speak("Sorry, I couldn't fetch a fact right now.")

def tell_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")
    result_box.insert(tk.END, "The current time is " + current_time + "\n")

def wikipedia_search(query):
    try:
        summary = wikipedia.summary(query, sentences=3)
        speak(summary)
        result_box.insert(tk.END, summary + "\n")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("The topic is ambiguous. Here are some options:")
        options = ", ".join(e.options[:5])
        speak(options)
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any information on that topic.")

def open_website():
    webbrowser.open("https://www.google.com")
    speak("Opening Google website.")

def execute_command(command):
    command = command.lower()

 # Weather Queries (Expanded)
    if "weather" in command:
        location = None

        # Clean up input for various phrases
        if "current weather in" in command:
            location = command.replace("current weather in", "").strip()
        elif "weather in" in command:
            location = command.replace("weather in", "").strip()
        elif "weather of" in command:
            location = command.replace("weather of", "").strip()

        if location:
            get_weather(location)
        else:
            speak("Please specify a location.")


    if any(query in command for query in ["tell me a joke", "make me laugh", "another joke", "funny joke", "give me a joke"]):
        tell_joke()

    elif any(query in command for query in ["news", "what's the news", "today's news", "current news", "headlines", "breaking news"]):
        get_news()

    elif any(query in command for query in ["fact", "give me a fact", "tell me something interesting", "fun fact", "random fact", "tell me a cool fact"]):
        get_fact()

    elif any(query in command for query in ["time", "what time is it", "current time", "tell me the time", "what's the time", "clock time"]):
        tell_time()

    elif any(query in command for query in ["wikipedia", "search on Wikipedia", "Wikipedia about", "look up", "find info on", "what does Wikipedia say about"]):
        query = command.replace("wikipedia", "").replace("search on Wikipedia", "").strip()
        wikipedia_search(query)

    elif any(query in command for query in ["calculate", "do the math", "math problem", "can you calculate", "solve this", "find the result of"]):
        expression = command.replace("calculate", "").strip()
        calculate(expression)


    elif "open google" in command:
        open_website()

    elif "exit" in command or "bye" in command or "quit" in command:
        speak("Goodbye!")
        root.quit()

    else:
        speak("Sorry, I didn't understand that command.")
        
def initialize_gui():
    def process_command():
        user_command = command_entry.get()
        if not user_command.strip():
            messagebox.showwarning("Input Error", "Please enter a command.")
            return

        display_input_output(f"You: {user_command}")

        # Add all query handlers here
        try:
            if any(query in user_command for query in ["tell me a joke", "make me laugh", "another joke", "funny joke", "give me a joke"]):
                tell_joke()

            elif any(query in user_command for query in ["news", "what's the news", "today's news", "current news", "headlines", "breaking news"]):
                get_news()

            elif any(query in user_command for query in ["fact", "give me a fact", "tell me something interesting", "fun fact", "random fact", "tell me a cool fact"]):
                get_fact()

            elif any(query in user_command for query in ["time", "what time is it", "current time", "tell me the time", "what's the time", "clock time"]):
                tell_time()

            elif any(query in user_command for query in ["wikipedia", "search on Wikipedia", "Wikipedia about", "look up", "find info on", "what does Wikipedia say about"]):
                query = user_command.replace("wikipedia", "").strip()
                wikipedia_search(query)

            elif any(query in user_command for query in ["calculate", "do the math", "math problem", "can you calculate", "solve this", "find the result of"]):
                expression = user_command.replace("calculate", "").strip()
                calculate(expression)

            else:
                display_input_output(f"Bot: Sorry, I don't understand the command '{user_command}'.")
        except Exception as e:
            display_input_output(f"Bot: There was an error processing your command. {str(e)}")

    # Function to display input and output in the GUI
    def display_input_output(message):
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, message + "\n")
        output_box.config(state=tk.DISABLED)
        output_box.see(tk.END)

    # Create the main window
    root = tk.Tk()
    root.title("Virtual Assistant")
    root.geometry("600x400")

    # Add a label
    label = tk.Label(root, text="Enter your command:", font=("Helvetica", 14))
    label.pack(pady=10)

    # Entry box for user input
    command_entry = tk.Entry(root, font=("Helvetica", 14), width=50)
    command_entry.pack(pady=10)

    # Button to process the command
    submit_button = tk.Button(root, text="Submit", font=("Helvetica", 14), command=lambda: threading.Thread(target=process_command).start())
    submit_button.pack(pady=10)

    # Scrolled Text box to display input and output
    output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), state=tk.DISABLED, height=15)
    output_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)        

def listen_for_commands():
    while True:
        command = listen()
        if command:
            execute_command(command)

thread = threading.Thread(target=listen_for_commands, daemon=True)
thread.start()

root.mainloop()
