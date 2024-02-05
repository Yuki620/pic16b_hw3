from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def submit():
    return render_template('submit.html')