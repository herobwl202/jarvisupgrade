# GUI3.py
from PyQt5 import QtWidgets
from JarvisUI import Ui_MainWindow
import pyttsx3 as p
from NeuralNetwork import bag_of_words, tokenize
from Brain import NeuralNet
import torch
import random
import json
import sys
import threading
import speech_recognition as sr
import datetime
from selenium_web import infow
from YT_auto import music
from Speak import Say
from News import news
import randfacts
from jokes import joke
from weather import get_weather
from Task import NonInputExecution
import dateparser
import pyautogui
import sys


sys.setrecursionlimit(200)

class GUIApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(GUIApp, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handle_start_button)
        self.pushButton_2.clicked.connect(self.handle_exit_button)
        self.paused = False  # Thêm biến trạng thái
        self.should_exit = False  # Thêm biến thoát

        # Initialize the voice assistant components
        self.engine = p.init()
        self.rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 170)
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)

        # Load intents from JSON file
        with open("intents.json", 'r') as json_data:
            self.intents = json.load(json_data)
##
        # Load neural network model and related data
        FILE = "TrainData.pth"
        data = torch.load(FILE)

        self.input_size = data["input_size"]
        self.hidden_size = data["hidden_size"]
        self.output_size = data["output_size"]
        self.all_words = data["all_words"]
        self.tags = data["tags"]
        self.model_state = data["model_state"]

        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size)
        self.model.load_state_dict(self.model_state)
        self.model.eval()

        # Initialize self.Terminal
        self.Terminal.setText("<p>Welcome to JARVIS Terminal</p>")

        # Thêm biến thread để lắng nghe âm thanh
        self.listen_thread = threading.Thread(target=self.run_voice_assistant)

    def handle_start_button(self):
        # Kiểm tra nếu thread chưa chạy, bắt đầu nó
        if not self.listen_thread.is_alive():
            self.listen_thread.start()

    def handle_exit_button(self):
        # Đặt biến thoát để kết thúc vòng lặp lắng nghe
        self.should_exit = True


    def set_alarm(self, time_str, date_str, message):
        try:
            alarm_time = dateparser.parse(f"{date_str} {time_str}")
            
            if alarm_time:
                current_time = datetime.datetime.now()
                
                if alarm_time > current_time:
                    delta = (alarm_time - current_time).total_seconds()
                    threading.Timer(delta, self.trigger_alarm, args=[message]).start()
                    print(f"Alarm set for {alarm_time}")
                else:
                    print("Invalid alarm time. Please set a future time.")
            else:
                print("Invalid date or time format. Please try again.")
        except ValueError:
            print("Invalid date or time format. Please try again.")

    def get_jarvis_response(self, sentence):
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    reply = random.choice(intent["responses"])

                    if "time" in reply:
                        NonInputExecution(reply)

                    elif "date" in reply:
                        NonInputExecution(reply)

                    elif "day" in reply:
                        NonInputExecution(reply)

                    else:
                        Say(reply)

    def run_voice_assistant(self):
        def speak(text):
            self.engine.say(text)
            self.engine.runAndWait()

        def wishme():
            hour = int(datetime.datetime.now().hour)
            if hour < 12:
                return "morning"
            elif 12 <= hour < 18:
                return "afternoon"
            else:
                return "evening"

        speak("Hello, good " + wishme() + ", I'm JARVIS.")
        speak("How are you feeling?")

        recognizer = sr.Recognizer()

        while not self.should_exit:
            try:
                with sr.Microphone() as source:
                    recognizer.energy_threshold = 10000
                    recognizer.adjust_for_ambient_noise(source, 1.2)
                    print("Listening...")
                    audio = recognizer.listen(source)
                    text2 = recognizer.recognize_google(audio)
                    print(text2)

                    if "information" in text2:
                        speak("You need information related to which topic?")
                        with sr.Microphone() as source:
                            recognizer.energy_threshold = 10000
                            recognizer.adjust_for_ambient_noise(source, 1.2)
                            print("Listening...")
                            audio = recognizer.listen(source)
                            infor = recognizer.recognize_google(audio)
                        assist = infow()
                        info_text = assist.get_info(infor)
                        print(info_text)
                        speak(info_text)

                    elif "play" in text2 and "video" in text2:
                        speak("You want me to play which video?")
                        with sr.Microphone() as source:
                            recognizer.energy_threshold = 10000
                            recognizer.adjust_for_ambient_noise(source, 1.2)
                            print("Listening...")
                            audio = recognizer.listen(source)
                            vid = recognizer.recognize_google(audio)
                            print("Playing {} on Youtube".format(vid))
                            assist = music()
                            assist.play(vid)

                    elif "news" in text2:
                        print("Sure, sir. Now I will read news for you.")
                        speak("Sure, sir. Now I will read news for you.")
                        arr = news()
                        for i in range(len(arr)):
                            print(arr[i])
                            speak(arr[i])

                    elif "joke" in text2 or "jokes" in text2:
                        speak("Sure, sir, get ready for some chuckles")
                        arr = joke()
                        print(arr[0])
                        speak(arr[0])
                        print(arr[1])
                        speak(arr[1])

                    elif "fact" in text2 or "facts" in text2:
                        speak("Sure, sir.")
                        x = randfacts.get_fact()
                        print(x)
                        speak("Did you know that, " + x)

                    elif "weather" in text2.lower():
                        temperature, description = get_weather()
                        print(temperature, description)
                        speak(f"Temperature in Vietnam is {temperature} degree Celsius and with {description}")

                    elif 'full' in text2 or "screen" in text2:
                        assist.press_key('F')
                        print("Ok")
                        speak("Ok")

                    elif 'skip' in text2 or "advertisement" in text2:
                        # Đặt biến xpath trước khi sử dụng nó
                        xpath = ".//div/div/div/div/div/span/button/div[contains(text(),'Skip Ad')]"
                        assist.click_button_by_xpath(xpath)
                        print("Right away")
                        speak("Right away")

                    elif 'back' in text2 or 'previous' in text2:
                        pyautogui.hotkey('alt', 'left')
                        print("Shall I proceed.")
                        speak("Shall I proceed.")

                    elif 'right' in text2:
                        pyautogui.hotkey('alt', 'right')
                        print("As you wish")
                        speak("As you wish")

                    elif 'subtitle' in text2 or 'subtitles' in text2:
                        pyautogui.hotkey('c')
                        print("I've located the target")
                        speak("I've located the target.")

                    elif 'stop' in text2 or 'start' in text2:
                        pyautogui.hotkey('space')
                        print("The situation is under control.")
                        speak("The situation is under control.")

                    elif 'next' in text2 or 'next video' in text2:
                        pyautogui.hotkey('shift', 'n')
                        print("Yes. I'm working on it.")
                        speak("Yes I'm working on it.")

                    elif 'close' in text2 or 'close it' in text2:
                        pyautogui.hotkey('alt', 'f4')
                        print("As you wish.")
                        speak("As you wish.")

                    elif "set an alarm" in text2:
                        speak("Sure, sir. What time would you like to set the alarm?")
                        with sr.Microphone() as source:
                            recognizer.energy_threshold = 10000
                            recognizer.adjust_for_ambient_noise(source, 1.2)
                            print("Listening...")
                            audio = recognizer.listen(source)
                            alarm_time = recognizer.recognize_google(audio)
                        
                        speak("When would you like to set the alarm?")
                        with sr.Microphone() as source:
                            recognizer.energy_threshold = 10000
                            recognizer.adjust_for_ambient_noise(source, 1.2)
                            print("Listening...")
                            audio = recognizer.listen(source)
                            alarm_date = recognizer.recognize_google(audio)
                        
                        speak("What message would you like for the alarm?")
                        with sr.Microphone() as source:
                            recognizer.energy_threshold = 10000
                            recognizer.adjust_for_ambient_noise(source, 1.2)
                            print("Listening...")
                            audio = recognizer.listen(source)
                            alarm_message = recognizer.recognize_google(audio)
                        
                        self.set_alarm(alarm_time, alarm_date, alarm_message)
                       

                    self.get_jarvis_response(text2)

            except sr.UnknownValueError:
                pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = GUIApp()
    mainWindow.show()
    sys.exit(app.exec_())