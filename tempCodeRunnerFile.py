import pyttsx3
import speech_recognition as sr
from datetime import datetime
import wikipedia
import requests  # import requests for weather apis
import pyjokes
from newsapi import NewsApiClient
import tkinter as tk 
from tkinter import scrolledtext
import os 
import webbrowser
import json
import random


root = tk.Tk()  # Create the main window
root.title("Tkinter Test Window")  # Set the window title
root.geometry("300x200")  # Set the window size

label = tk.Label(root, text="Hello, Tkinter!")  # Create a label widget
label.pack()  # Pack the label widget into the window

engine = pyttsx3.init()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# listen function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your command...")
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

#jokes
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    result_box.insert(tk.END, joke + "\n")
    
# Function to get latest news
def get_news():
    try:
        api = NewsApiClient(api_key='YOUR_NEWSAPI_KEY')  # Replace with your API key
        headlines = api.get_top_headlines(language='en')
        articles = headlines['articles'][:5]  # Get top 5 articles
        news = "Here are the top 5 news headlines: "
        for article in articles:
            news += article['title'] + ". "
        speak(news)
    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("Sorry, I couldn't fetch the news right now.")    

# Function to get a random fact
def get_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        fact = response.json().get("text", "Sorry, I couldn't fetch a fact right now.")
        speak(fact)
        result_box.insert(tk.END, fact + "\n")
    except Exception as e:
        print(f"Error fetching fact: {e}")
        speak("Sorry, I couldn't fetch a fact right now.")
        result_box.insert(tk.END, fact + "\n")
        
            
# weather function
def get_weather(location):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=63d033c6d2ff634bff145bd6ec0b473a&units=metric"
        response = requests.get(url)

        # Check if response status is 200 (successful)
        if response.status_code == 200:
            data = response.json()  # Parse the response JSON
            main = data.get("main", {})
            weather = data.get("weather", [{}])[0]
            temperature = main.get("temp")
            humidity = main.get("humidity")
            description = weather.get("description")

            if temperature and humidity and description:
                speak(f"The current temperature in {location} is {temperature} degrees Celsius with {description}. The humidity level is {humidity} percent.")
            else:
                speak("I couldn't retrieve complete weather data.")
        else:
            # If response is not successful, handle the error
            speak(f"Could not retrieve weather data for {location}. Please check the city name or try again later.")
            result_box.insert(tk.END, f"The weather in {location} is {weather_desc} with a temperature of {temp} Kelvin.\n")

    except Exception as e:
        print(f"Error occurred: {e}")
        speak("Sorry, I couldn't fetch the weather information.")

# time function
def tell_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")  # Format the time in hours and minutes
    speak(f"The current time is {current_time}")
    result_box.insert(tk.END, "The current time is " + current_time + "\n")

# basic calculations function
def calculate(command):
    try:
        # Replace words with symbols to make it easier to parse
        command = command.replace("plus", "+")
        command = command.replace("minus", "-")
        command = command.replace("times", "*")
        command = command.replace("into", "*")
        command = command.replace("divided by", "/")
        command = command.replace("divide by", "/")

        # Evaluate the expression
        result = eval(command)
        speak(f"The result is {result}")
    except Exception as e:
        speak("Sorry, I could not calculate that.")

# wikipedia search function
# Improved Wikipedia search function
def wikipedia_search(query):
    try:
        # Search Wikipedia and get a more detailed summary (max 3 sentences)
        summary = wikipedia.summary(query, sentences=3)  
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation error and suggest options
        speak("The topic is ambiguous. Here are some options:")
        options = ", ".join(e.options[:5])  # Show first 5 options
        speak(options)
    except wikipedia.exceptions.PageError:
        # Handle page not found error
        speak("Sorry, I couldn't find any information on that topic.")
    except Exception as e:
        # Catch any other errors
        print(f"Error: {e}")
        speak("Sorry, there was an error while fetching the information.")
        result_box.insert(tk.END, "Error: Wikipedia unreachable.\n")

# Function to open a website
def open_website():
    webbrowser.open("https://www.google.com")
    speak("Opening Google website.")

# GUI Setup
root = tk.Tk()
root.title("Virtual Assistant")

# Create a frame for the result display
frame = tk.Frame(root)
frame.pack(pady=10)

# Create a scrolled text box for results
result_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
result_box.grid(row=0, column=0, padx=5, pady=5)

# Create a scrolled text box for command input display
command_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=5, font=("Arial", 12), bg="#f0f0f0")
command_box.grid(row=1, column=0, padx=5, pady=5)

# Create a status label to show assistant's listening status
status_label = tk.Label(root, text="Ready to assist!", font=("Arial", 12), fg="green")
status_label.pack(pady=5)

# main code
if __name__ == "__main__":
    speak("Hello! I am your virtual assistant. How can I help you?")
    while True:
        command = listen()
        if command:
            command = command.lower()  # Convert to lowercase for easier matching

            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            
            elif "time" in command:
                tell_time()
            elif "what time is it" in command:
                tell_time() 
            elif "tell me the time" in command:
                tell_time()    
            elif "current time" in command:
                tell_time()
            elif "show me the time" in command:
                tell_time()
            elif "time please" in command:
                tell_time()
            elif "tell me what time it is" in command:
                tell_time()
            elif "can you tell me the time" in command:
                tell_time()
            elif "give me the time" in command:
                tell_time()
            elif "what's the time" in command:
                tell_time()    
                
            elif "calculate" in command:
                calculate(command.replace("calculate", ""))
            elif "how much is" in command:
                calculate(command.replace("how much is", ""))
            elif "what is" in command:
                calculate(command.replace("what is", ""))
            elif "solve" in command:
                calculate(command.replace("solve", ""))
            elif "compute" in command:
                calculate(command.replace("compute", ""))
            elif "find" in command:
                calculate(command.replace("find", ""))
            elif "can you calculate" in command:
                calculate(command.replace("can you calculate", ""))
            elif "please calculate" in command:
                calculate(command.replace("please calculate", ""))
            elif "give me the answer" in command:
                calculate(command.replace("give me the answer", ""))
            elif "how to calculate" in command:
                calculate(command.replace("how to calculate", ""))
                
                
            elif "wikipedia" in command:
                query = command.replace("wikipedia", "").strip()
                wikipedia_search(query)
            elif "search on wikipedia" in command:
                query = command.replace("search on wikipedia", "").strip()
                wikipedia_search(query)
            elif "find on wikipedia" in command:
                query = command.replace("find on wikipedia", "").strip()
                wikipedia_search(query)
            elif "get me information on" in command:
                query = command.replace("get me information on", "").strip()
                wikipedia_search(query)
            elif "what is" in command:
                query = command.replace("what is", "").strip()
                wikipedia_search(query)
            elif "tell me about" in command:
                query = command.replace("tell me about", "").strip()
                wikipedia_search(query)
            elif "who is" in command:
                query = command.replace("who is", "").strip()
                wikipedia_search(query)
            elif "explain" in command:
                query = command.replace("explain", "").strip()
                wikipedia_search(query)
            elif "give me details about" in command:
                query = command.replace("give me details about", "").strip()
                wikipedia_search(query)
            elif "look up" in command:
                query = command.replace("look up", "").strip()
                wikipedia_search(query)
                
                
            elif "weather" in command:
                # Check for different weather query formats
                if "what is the weather of" in command or "what's the weather of" in command:
                    location = command.replace("what is the weather of", "").replace("what's the weather of", "").strip()
                    if location:
                        get_weather(location)
                    else:
                        speak("Please specify a location.")
                elif "weather" in command:
                    location = command.replace("weather", "").replace("in", "").strip()
                    if location:
                        get_weather(location)
                    else:
                        speak("Please specify a location.")
                        
                        
            elif "joke" in command:
                tell_joke()
            elif "tell me a joke" in command:
                tell_joke()
            elif "say something funny" in command:
                tell_joke()
            elif "make me laugh" in command:
                tell_joke()
            elif "give me a joke" in command:
                tell_joke()
            elif "can you tell me a joke" in command:
                tell_joke()
            elif "joke please" in command:
                tell_joke()
            elif "crack a joke" in command:
                tell_joke()
            elif "humor me" in command:
                tell_joke()
            elif "can you make me laugh" in command:
                tell_joke()
                
                
            elif "fact" in command:
                get_fact()
            elif "give me a fact" in command:
                get_fact()
            elif "tell me a fact" in command:
                get_fact()
            elif "random fact" in command:
                get_fact()
            elif "can you tell me a fact" in command:
                get_fact()
            elif "fact please" in command:
                get_fact()
            elif "give me something interesting" in command:
                get_fact()
            elif "tell me something cool" in command:
                get_fact()
            elif "what's a fun fact" in command:
                get_fact()
            elif "surprise me with a fact" in command:
                get_fact()
                
                
            elif "news" in command:
                get_news()    
            elif "latest news" in command:
                get_news()
            elif "what's happening in the world" in command:
                get_news()
            elif "show me the news" in command:
                get_news()
            elif "news update" in command:
                get_news()
            elif "tell me the latest news" in command:
                get_news()
            elif "what are the news headlines" in command:
                get_news()
            elif "what's the latest news" in command:
                get_news()
            elif "current news" in command:
                get_news()
            elif "headlines" in command:
                get_news()
                
                      
            else:
                speak("I'm sorry, I can't help with that yet.")
                result_box.insert(tk.END, "I can't help with that yet.\n")


listen_button = tk.Button(root, text="Start Listening", command=process_command, width=20, height=2, font=("Arial", 14), bg="#4CAF50", fg="white")
listen_button.pack(pady=20)

# Start the GUI loop
root.mainloop()