import sys
import pyttsx3
import speech_recognition as sr
import json
import os
import datetime
import face_rec_hog as fr
import random
import spotipy
from PyQt6.QtWidgets import QApplication,    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QTextEdit
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QIcon, QKeyEvent
from PyQt6.QtCore import Qt, QTimer
from spotipy.oauth2 import SpotifyOAuth
from screen_brightness_control import get_brightness,set_brightness
import platform
import datetime
import socket
import os
import psutil
from pathlib import Path
import locale
import pyautogui
import requests


#open weather creds
api_key="06cd0e4c7fb5bfd9c3b85ac354dda54a"
city= "Greater Noida,IN"
base_url="http://api.openweathermap.org/data/2.5/weather?"
complete_url = f"{base_url}q={city}&appid={api_key}&units=jaimetric"  



#Spotify creds
CLIENT_ID = "2f3bda59118145fbb3e3c319026eec4b"
CLIENT_SECRET = "6ab80428f270430893ec1cc8676d6d84"
REDIRECT_URI = "http://localhost:8080"

scope = "user-modify-playback-state user-read-playback-state"


try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=scope))
    print("Access token is valid.")
    devices = sp.devices()
    print("Available devices:", devices)
except Exception as e:
    print(f"Error validating token or fetching devices: {e}")




engine = pyttsx3.init()
engine.setProperty('rate', 200)
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  


def tts(text):
    """Speak the provided text using the TTS engine."""
    print(text)
    engine.say(text)
    engine.runAndWait()


def load_or_create_profile(user_name):
    profile_file = f"{user_name}_profile.json"
    if os.path.exists(profile_file):
        with open(profile_file, "r") as file:
            profile = json.load(file)
            profile["Last_Login"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(profile_file, "w") as file:
                json.dump(profile, file, indent=4)
            return profile
    else:
        return create_user_profile(user_name)

def create_user_profile(user_name):
    profile = {
        "Name": user_name,
        "Settings": {
            "Current_Resolution": f"{pyautogui.size()}",
            "Current_OS": f"{platform.system()} ({platform.release()})",
            "Theme": "Dark",
            "Notifications": "Enabled",
            "Language": f"{locale.getdefaultlocale()[0]}",
            "CPU_Cores": psutil.cpu_count(logical=True),
            "Memory_Usage": f"{psutil.virtual_memory().percent}%",
            "Disk_Usage": f"{psutil.disk_usage('/').percent}%",
            "IP_Address": socket.gethostbyname(socket.gethostname()),
            "Home_Directory": str(Path.home())
        },
        "Last_Login": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(f"{user_name}_profile.json", "w") as file:
        json.dump(profile, file, indent=4)
    tts("Profile created successfully!")
    return profile

def safe_disconnect(signal):
         """Safely disconnect all slots connected to the signal."""
         try:
            signal.disconnect()
         except TypeError:
            pass  
class SmoothBlinkingGlowingEyes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AVA")
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("background-color: #000000;")
        self.setWindowIcon(QIcon(r'C:\Users\jashn\Pictures\Screenshots\Screenshot 2025-01-03 003300.png'))
        self.initUI()

    def initUI(self):
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        
        face_layout = QVBoxLayout()
        face_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Face display (eyes)
        self.face_label = QLabel(self)
        self.face_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.face_label.setFixedSize(400, 300)  
        face_layout.addWidget(self.face_label)

        
        self.layout.addLayout(face_layout)

        # Chatbox above the buttons
        self.chatbox = QTextEdit(self)
        self.chatbox.setPlaceholderText("Chat with Juno...")
        self.chatbox.setStyleSheet("""
            background-color: #333;
            color: white;
            border-radius: 15px;
            font-size: 16px;
            padding: 10px;
            border: 2px solid #555;
        """)
        self.chatbox.setReadOnly(True)
        self.chatbox.setFixedHeight(180)  
        self.layout.addWidget(self.chatbox)

        
        input_layout = QHBoxLayout()

        # Start button
        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 25px;
                font-size: 18px;
                padding: 15px 30px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003366;
            }
        """)
        self.start_button.clicked.connect(self.startConversation)

        # Textbox
        self.text_box = QLineEdit(self)
        self.text_box.setPlaceholderText("Enter your message...")
        self.text_box.setStyleSheet("""
            background-color: #333;
            color: white;
            border-radius: 20px;
            font-size: 16px;
            padding: 10px;
            border: 2px solid #555;
        """)
        self.text_box.setFixedHeight(40)

        # Send button
        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 20px;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003366;
            }
        """)
        self.send_button.clicked.connect(self.sendMessage)

        
        input_layout.addWidget(self.start_button)
        input_layout.addWidget(self.text_box)
        input_layout.addWidget(self.send_button)

        
        self.layout.addLayout(input_layout)

        
        self.central_widget.setLayout(self.layout)

        
        self.blinking = False
        self.blink_progress = 0
        self.blink_direction = 1

        
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.updateBlinking)
        self.animation_timer.start(16)  
        self.initQuiz()

        
        self.drawFace()
        

        
        self.user_profile = fr.recognize_or_register_face()

    def keyPressEvent(self, event: QKeyEvent):
        """Override the key press event to detect Enter key."""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.sendMessage()
    
    def startBlinking(self):
        """Start the blinking animation."""
        if not self.blinking:
            self.blinking = True
            self.blink_progress = 0
            self.blink_direction = 1  # Start closing

    def updateBlinking(self):
        """Update the blinking animation frame by frame."""
        if self.blinking:
            
            self.blink_progress += self.blink_direction * 6

            
            if self.blink_progress >= 100:  # Fully closed
                self.blink_direction = -1  # Start opening
            elif self.blink_progress <= 0:  # Fully open
                self.blinking = False  # End animation

            # Redraw the face 
            self.drawFace()

    def drawFace(self):
        """Draw the face with smooth blinking and glowing square eyes."""
        pixmap = QPixmap(self.face_label.size())
        pixmap.fill(Qt.GlobalColor.black)
        painter = QPainter(pixmap)

        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            
            glow_color = QColor(0, 255, 255, 100)
            eye_color = QColor(0, 255, 255)

            
            eye_height = max(10, 60 - int(self.blink_progress * 0.6))

            # Left Eye
            painter.setBrush(QBrush(glow_color))
            painter.drawRect(90, 110, 80, 80)
            painter.setBrush(QBrush(eye_color))
            painter.drawRect(100, 120 + (60 - eye_height) // 2, 60, eye_height)
                        # Right Eye
            painter.setBrush(QBrush(glow_color))
            painter.drawRect(230, 110, 80, 80)
            painter.setBrush(QBrush(eye_color))
            painter.drawRect(240, 120 + (60 - eye_height) // 2, 60, eye_height)

        finally:
            painter.end()

        self.face_label.setPixmap(pixmap)
    def startConversation(self):
        """Start the conversation and load or create the user profile."""
        self.start_button.hide()

        user_name = self.user_profile #Face Recognition
        self.user_profile = load_or_create_profile(user_name)
        greetings = [
    f"Yo {self.user_profile['Name']}! What's cookin'?",
    f"Sup, {self.user_profile['Name']}? Ready to conquer the day?",
    f"Well, well, well, if it isn’t the one and only {self.user_profile['Name']}!",
    f"Hey hey hey, {self.user_profile['Name']}! What’s the vibe today?",
    f"{self.user_profile['Name']} in the house! Let’s make magic happen.",
    f"What’s up, legend? Oh wait, it’s you, {self.user_profile['Name']}!",
    f"Hey superstar {self.user_profile['Name']}! What’s your next big move?",
    f"Drumroll please… 🥁 It’s {self.user_profile['Name']}! How’s it going?",
    f"Greetings, mortal! Or should I say, legendary {self.user_profile['Name']}?",
    f"Ahoy, {self.user_profile['Name']}! What adventures await today?",
    f"Rise and shine, {self.user_profile['Name']}! Let’s get this party started.",
    f"Knock knock. Who’s there? Oh, it’s {self.user_profile['Name']}—the star of the show!",
    f"Hello, Commander {self.user_profile['Name']}! What’s our mission today?",
    f"{self.user_profile['Name']}, you’ve arrived! The fun can officially begin.",
    f"Brace yourself, {self.user_profile['Name']} is here! Let’s rock this.",
    f"Hey {self.user_profile['Name']}! What mischief are we planning today?",
    f"Guess who’s back? Back again. It’s {self.user_profile['Name']}—tell a friend!",
    f"Buckle up, {self.user_profile['Name']}! We’re about to make things epic.",
    f"Look who decided to show up—{self.user_profile['Name']}! Let’s do this."
]
        greet_choice=random.choice(greetings)
        self.chatbox.append(f"Juno: {greet_choice}")
        tts(f"{greet_choice}")
        

    def sendMessage(self):
        """Handle the user's input message."""
        user_input = self.text_box.text().strip()
        if not user_input:
            return  

        if user_input:
            self.chatbox.append(f"You: {user_input}")
            self.text_box.clear()
            if self.is_in_quiz:
                self.checkAnswer(user_input)
            elif "search" in user_input.lower():
                self.initiateSearch()
            
            elif "game" in user_input.lower():
                self.games()

            elif "weather" in user_input.lower():
                response = requests.get(complete_url)
                data = response.json()
                if data["cod"] == 200:
                
                 main = data["main"]
                 wind = data["wind"]
                 weather = data["weather"][0]
                 
                 temperature = main["temp"]
                 humidity = main["humidity"]
                 pressure = main["pressure"]
                 wind_speed = wind["speed"]
                 description = weather["description"]
                 
                 
                 weather_report = f"""
                 Weather Details for {city}:
             
                 Temperature: {temperature}°C
                 Humidity: {humidity}%
                 Pressure: {pressure} hPa
                 Wind Speed: {wind_speed} m/s
                 Weather: {description.capitalize()}
                 """
                 self.chatbox.append(weather_report)
                 tts(weather_report)
            
            #elif "increase" in user_input.lower() and "volume" in user_input.lower():
                # os.system(f'"{nirpath}" changesysvolume {5000}')
                # self.chatbox.append("Increased Volume.")
                # tts("increased volume")

            #elif "decrease" in user_input.lower() and "volume" in user_input.lower():
                # os.system(f'"{nirpath}" changesysvolume -{5000}')
                # self.chatbox.append("Decreased Volume.")
                # tts("decreased volume")

            elif "news" in user_input.lower():
                    url = 'https://newsapi.org/v2/everything'
                    params = {
                            'q': 'Noida',
                            'from': '2024-12-31',
                            'to': '2024-12-31',
                            'language': 'en',
                            'apiKey': '1730ef75dc07473e848e7d67c704d4b7'
                        }
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        news_data = response.json()
                        articles = news_data.get('articles', [])
                        if articles:
                            tts("here's today's news")
                            for article in articles:
                                self.chatbox.append(f"Title: {article['title']}")
                                self.chatbox.append(f"Description: {article['description']}")
                                self.chatbox.append(f"URL: {article['url']}")   
                                self.chatbox.append('-' * 80)
                        else:
                            self.chatbox.append("No news articles found for Noida today.")
                            tts("No news articles found for Noida today.")
                    else:
                        self.chatbox.append(f"Failed to fetch news: {response.status_code} - {response.text}")
                        tts(f"Failed to fetch news: {response.status_code} - {response.text}")
            
            elif "play" in user_input.lower():
                x=user_input.split("play")
                self.play_song(x[1])
                
            elif "about" in user_input.lower() and "yourself" in user_input.lower():
                about=f"""{self.user_profile['Name']}, I’m Juno! 
I’m a smart and versatile assistant created by Jai Saraswat and Jash Nankani. Here’s what I can do for you:

🌞 Adjust Brightness: Easily increase or decrease your screen brightness.
🎵 Play Songs: Enjoy music anytime with my playlist control.
🧠 Face Recognition: Recognize faces like a pro for smart interactions.
🎮 Play Games: Dive into fun games and keep boredom at bay.
📰 News: Know what's happening in your area currently!! 
☁️ Weather: Well it's cold today.
😎 Profile:Create profiles based on your system.
📱 I can Open Applications too!
😂 Tell Jokes: To keep you entertained!

I’m here to make your life easier and more entertaining. Just ask, and I’ll get it done!"""
                self.chatbox.append(about)
                tts(about)

            elif "increase" in user_input.lower() and "brightness" in user_input.lower():
                try: 
                    cb=get_brightness()
                    cb=cb[0]
                    set_brightness(cb+20)    
                    self.chatbox.append("Increased brightness Sir.")
                    tts("Increased brightness Sir.")
                except Exception as e:
                    self.chatbox.append(f"Not able to increase brightness({e}).")
            
            elif "decrease" in user_input.lower() and "brightness" in user_input.lower():
                try: 
                    cb=get_brightness()
                    cb=cb[0]
                    set_brightness(cb-20)    
                    self.chatbox.append("decreased brightness Sir.")
                    tts("decreased brightness Sir.")
                except Exception as e:
                    self.chatbox.append(f"Not able to decrease brightness({e}).")
            

            else:
                self.processCommand(user_input)

        
        else:
            tts("")


    
    def play_song(self,song_name):
        try:
            
            results = sp.search(q=song_name, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                track_uri = track['uri']

                
                devices = sp.devices()
                if not devices['devices']:
                    print("No active Spotify device found. Please open Spotify on a device.")
                    return
            
                
                device_id = devices['devices'][0]['id']
                sp.start_playback(device_id=device_id, uris=[track_uri])
                print(f"Playing: {track['name']} by {track['artists'][0]['name']}")
                self.chatbox.append(f"Playing: {track['name']} by {track['artists'][0]['name']}")
                tts(f"Playing: {track['name']} by {track['artists'][0]['name']}")
            else:
                print("Song not found on Spotify.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def games(self):
        tts("Alright! Let's play a game. What do you want to play: Number Guessing or Trivia Quiz?")
        self.chatbox.append("Alright! Let's play a game. What do you want to play: Number Guessing or Word Guessing or Trivia Quiz?")
    
        
        safe_disconnect(self.text_box.returnPressed)

        
        self.text_box.returnPressed.connect(self.handleGameChoice)


    def handleGameChoice(self):
        game_choice = self.text_box.text().strip()
        self.text_box.clear()

        if 'number' in game_choice.lower() and 'guessing' in game_choice.lower():
            self.number_guessing_game()

        elif 'trivia' in game_choice.lower() and 'quiz' in game_choice.lower():
            self.startQuiz()

        else:
            tts("I didn't understand that. Let's start again.")
            self.chatbox.append("I didn't understand that. Let's start again.")
            self.games()  

    def startQuiz(self):
        """Start the trivia quiz."""
        self.is_in_quiz = True
        self.current_question_index = 0
        self.quiz_score = 0

        
        safe_disconnect(self.text_box.returnPressed)

        
        self.text_box.returnPressed.connect(self.sendMessage)

        tts("Starting the Trivia Quiz! Answer the questions correctly.")
        self.chatbox.append("Starting the Trivia Quiz! Answer the questions correctly.\n")
        self.showNextQuestion()

    def showNextQuestion(self):
        """Display the next quiz question."""
        if self.current_question_index < len(self.trivia_questions):
            question = self.trivia_questions[self.current_question_index]["question"]
            self.chatbox.append(f"Question {self.current_question_index + 1}: {question}")
            tts(f"Question {self.current_question_index + 1}: {question}")
        else:
            self.endQuiz()

    def endQuiz(self):
        """End the trivia quiz and show the score."""
        self.is_in_quiz = False
        self.chatbox.append("\nThe quiz has ended!")
        self.chatbox.append(f"Your final score: {self.quiz_score}/{len(self.trivia_questions)}")
        tts(f"The quiz has ended! Your final score: {self.quiz_score}/{len(self.trivia_questions)}")
        self.chatbox.append("Type 'game' to play again or chat with me!")

    def checkAnswer(self, answer):
        """Check the user's answer and proceed to the next question."""
        correct_answer = self.trivia_questions[self.current_question_index]["answer"]
        if answer.lower() == correct_answer.lower():
            self.chatbox.append("Correct! 🎉")
            self.quiz_score += 1
            tts("Correct!")
        else:
            self.chatbox.append(f"Wrong! The correct answer was: {correct_answer}")
            tts(f"Wrong! The correct answer was: {correct_answer}")

        
        self.current_question_index += 1
        self.showNextQuestion()

    def initQuiz(self):
        """Initialize the trivia quiz questions and state."""
        self.trivia_questions = [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is 5 + 7?", "answer": "12"},
            {"question": "Who wrote 'Romeo and Juliet'?", "answer": "Shakespeare"},
            {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
            {"question": "What year did the Titanic sink?", "answer": "1912"},
        ]
        self.current_question_index = -1
        self.quiz_score = 0
        self.is_in_quiz = False 

    def number_guessing_game(self):
        self.chatbox.append("Welcome to the Number Guessing Game! I'm thinking of a number between 1 and 100. Try to guess it.")
        tts("Welcome to the Number Guessing Game! I'm thinking of a number between 1 and 100. Try to guess it.")
    
        self.target_number = random.randint(1, 100)
        self.attempts = 0

        
        safe_disconnect(self.text_box.returnPressed)

        
        self.text_box.returnPressed.connect(self.handleGuess)

    def handleGuess(self):
        user_input = self.text_box.text().strip()
        self.text_box.clear()

        try:
            guess = int(user_input)
        except ValueError:
            self.chatbox.append("Please enter a valid number.")
            tts("Please enter a valid number.")
            return

        self.attempts += 1

        if guess < self.target_number:
            self.chatbox.append("Too low! Try again.")
            tts("Too low! Try again.")
        elif guess > self.target_number:
            self.chatbox.append("Too high! Try again.")
            tts("Too high! Try again.")
        else:
            self.chatbox.append(f"Congratulations! You guessed the number in {self.attempts} attempts!")
            tts(f"Congratulations! You guessed the number in {self.attempts} attempts!")

            #safe_disconnect(self.text_box.returnPressed)
            self.text_box.returnPressed.disconnect()
            self.text_box.returnPressed.connect(self.sendMessage)
        

        
    def performSearch(self, query):
        """Perform the actual search logic."""
        
        tts(f"Searching for {query}. Please wait.")
        self.chatbox.append(f"Juno: Searching for '{query}'...")
    
        
        import webbrowser
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def initiateSearch(self):
        """Ask the user what they want to search for."""
        tts("What do you want to search for? Type 'exit search' to cancel.")
        self.chatbox.append("Juno: What do you want to search for? (Type 'exit search' to cancel)")
        self.text_box.setPlaceholderText("Type your search query here...")

         
        def handleSearch():
            search_query = self.text_box.text().strip()
            if search_query.lower() == "exit search":
                self.chatbox.append("Juno: Exiting search mode.")
                tts("Exiting search mode.")
                self.text_box.clear()
                self.text_box.setPlaceholderText("")  
                self.text_box.returnPressed.disconnect()  
            elif search_query:
                self.chatbox.append(f"You (Search): {search_query}")
                self.performSearch(search_query)
                self.text_box.clear() 
            else:
                tts("I didn't catch that. Please try again or type 'exit search' to cancel.")
                self.chatbox.append("Juno: Please try again or type 'exit search' to cancel.")

    
        self.text_box.returnPressed.connect(handleSearch)




    def processCommand(self, command):
        """Process the user's command and respond accordingly."""
        greet_words = ['hi', 'hello', 'hey']
        if any(word in command.lower() for word in greet_words):
            response = f"Hello {self.user_profile['Name']}! How can I help you?"
        elif 'time' in command.lower():
            now = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {now}."
    
    
        #For opening applications
        elif "open" in command.lower() and "calculator" in command.lower():
            os.system("calc")
            response="Opening calculator"

        elif "open" in command.lower() and "notepad" in command.lower():
            os.system("notepad")
            response="Opening Notepad"

        elif "time" in command.lower():
            time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response=f"Current time is: {time}"

        elif "name" in command.lower() and "your" in command.lower():
            response=f"My name is Chikki"

        elif "name" in command.lower() and "my" in command.lower():
            response=f"Your name is {self.user_profile['Name']}"

        
        elif 'tell' in command.lower() and 'joke' in command.lower():
            dark_jokes = [
     "Why don't graveyards have 4G? Because they're full of dead spots.",
     "I have a joke about a broken pencil... but it's pointless.",
     "I used to play piano by ear... but now I play it by the graveyard.",
     "Why don't skeletons fight each other? They don't have the guts.",
     "I told my wife she was drawing her eyebrows too high... She looked surprised.",
     "Why did the scarecrow win an award? Because he was outstanding in his field... until they found his body.",
     "I have a great joke about suicide... but it’s too dead to tell.",
     "What’s the difference between a snowman and a vampire? Snowmen melt, vampires turn to dust. One’s eternal, the other’s not.",
     "I’m reading a book on anti-gravity... It’s impossible to put down.",
     "Why don’t some couples go to the gym? Because some relationships don’t work out... like a dead body.",
     "What did one coffin say to the other? 'I’m going to miss you.'",
     "Why don’t you ever see hipsters at funerals? They’re too busy not caring.",
     "I started a company selling land mines… it’s going well, I’m making a killing.",
     "I told my friend 10 jokes to make him laugh... sadly, no pun in ten did.",
     "Why did the zombie go to therapy? He had too many unresolved issues.",
     "I’m terrified of the cemetery near my house. The headstones are so… *gravely* intimidating.",
     "The worst time to have a heart attack is during a game of charades.",
     "What’s the hardest part about being a ghost? Trying to get a decent job without any experience.",
     "I tried to write a joke about the Titanic... but it sank.",
     "If I had a penny for every time I said something stupid, I’d be rich… but I wouldn’t be here to spend it.",
     "I used to be a baker, but I couldn't make enough dough, so I quit… now I just loaf around.",
     ]
            joke_choice=random.choice(dark_jokes)
            response=joke_choice
        
        elif 'exit' in command.lower():
            response = "Goodbye! Exiting the application."
            tts(response)
            self.close()
            return
        else:
            response = "Sorry, I didn't understand that. Please try again!"

        self.chatbox.append(f"Juno: {response}")
        tts(response)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SmoothBlinkingGlowingEyes()
    main_window.show()

    QTimer.singleShot(2000, main_window.startBlinking)  
    blink_timer = QTimer(main_window)
    blink_timer.timeout.connect(main_window.startBlinking)
    blink_timer.start(3000)  
    
    sys.exit(app.exec())
