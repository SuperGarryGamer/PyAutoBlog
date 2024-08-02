from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "<h1>Welcome to PyAutoBlog :3</h1>"

@app.route("/favicon.ico")
def favicon():
    