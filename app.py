from flask import Flask, render_template, request, abort, redirect

app = Flask(__name__)
order_dict = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
