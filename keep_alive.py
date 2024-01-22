import os
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)


@app.route('/')
def index():
    return "To ensure your bot runs 24/7 on Replit, you can use services like Uptime Robot to ping the URL you get when you open the webview in a new page"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()
print("Bot Running!")
