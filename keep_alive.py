import os
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)


@app.route('/')
def index():
    return "To run this bot forever free you can use this Github Repo Made by Nick088 in Render for it to deploy using your own gemini api and discord bot token, or you can fork this for your modifications and use that instead, also use Uptime Robot to ensure it stays up"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()
print("Bot Running!")
