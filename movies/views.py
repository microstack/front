from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route('/movies/')
def movie_mainpage():
    return render_template('movies.html')
