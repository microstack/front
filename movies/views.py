from flask import Flask
app = Flask(__name__)

@app.route('/movies/')
def movie_mainpage():
    return "Hello movies!"
