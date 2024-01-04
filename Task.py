# Task.py
#Function
import datetime
from Speak import Say
import requests
import webbrowser as web
#2 Types

#1 - Non Input
#eg: Time, Date, Speedtest

def Time():
    time = datetime.datetime.now().strftime("%H:%M")
    Say(time)

def Date():
    date = datetime.date.today()
    Say(date)

def Day():
    day = datetime.datetime.now().strftime("%A")
    Say(day)

def NonInputExecution(query):
    
    query = str(query)

    if "time" in query:
        Time()
    
    elif "date" in query:
        Date()
    
    elif "day" in query:
        Day()