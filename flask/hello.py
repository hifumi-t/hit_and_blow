from flask import Flask
from flask import render_template

app = Flask(__name__)

bullets = [
    '箇条書き１',
    '箇条書き２',
    '箇条書き３',
    '箇条書き４',
    '箇条書き５',
    '箇条書き６',
    '箇条書き７',
    '箇条書き８',
    '箇条書き９'
]


@app.route("/")
def hello():
    return render_template('hello.html', bullets=bullets)
