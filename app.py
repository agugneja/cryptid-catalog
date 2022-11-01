from flask import Flask, render_template, request, abort, redirect

app = Flask(__name__)
order_dict = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')
@app.get('/profile')
def profile():
    return render_template('profile.html')

@app.get('/encyclopedia')
def encyclopedia():
    return render_template('encyclopedia.html')

@app.get('/sightings')
def sightings():
    return render_template('sightings.html')

@app.get('/logout')
def logout():
    return render_template('login.html')