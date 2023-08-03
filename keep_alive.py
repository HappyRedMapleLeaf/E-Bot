# web server stuff used in combination with uptimerobot to keep the repl on 24/7
# source: https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return ""

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
