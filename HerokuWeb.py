from operator import imod
import os
import ObonInstagramScraper
import datetime
import threading
import urllib.request
import time
from flask import Flask
from waitress import serve

app = Flask(__name__)

def ping():
    global isRunning
    time.sleep(1500) # 25 minutes
    while True:
        datetimeNowLocal = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        # running between 05.00 - 20.00, outside those hour let the app to sleep, to save free dyno hour on heroku
        if datetimeNowLocal.time() <= datetime.time(20,0,0) and datetimeNowLocal.time() >= datetime.time(5,0,0) and isRunning == "true":
            try:
                urllib.request.urlopen("https://ig-scrap-telegram-yuk-mengaji.herokuapp.com").read()
                print("Ping")
            except ValueError:
                print("Ping error: " + ValueError)
        else:
            print("I'ts time to sleep")
            break
        time.sleep(1500) # 25 minutes

@app.route("/start")
def start():   
    global isRunning
    datetimeNowLocal = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    # running between 05.00 - 20.00, outside those hour let the app to sleep, to save free dyno hour on heroku
    if datetimeNowLocal.time() <= datetime.time(20,0,0) and datetimeNowLocal.time() >= datetime.time(5,0,0) and isRunning == "false":
        isRunning = "true"
        threading.Thread(target=ping).start()
        threading.Thread(target=ObonInstagramScraper.start).start()
        return "App is running"
    else:
        if isRunning == "true":
            print("App still running")
            return "App still running"
        else:
            print("App can't running")
            return "App can't running"

@app.route("/")
def index():
    return "You didn't see anything"

if __name__ == "__main__":  
    global isRunning 
    isRunning = "false"
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)