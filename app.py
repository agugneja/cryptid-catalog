from flask import Flask, render_template, request, abort, redirect
from dotenv import load_dotenv
import os
from datetime import datetime
from src.models import Post, db

load_dotenv()

app = Flask(__name__)
order_dict = {}

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

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

def create_post():
    title = request.args.get('title')
    creature = request.args.get('creature')
    description = request.args.get('description')
    user_id = 1
    likes = 0
    dislikes = 0

    datetime = datetime.now()

    if not title or not creature or not description:
        abort(400)

    post = Post(title, creature, datetime, description, user_id, likes, dislikes)
    db.session.add(post)
    db.session.commit()

    return redirect('/sightings')

@app.get('/logout')
def logout():
    return render_template('login.html')