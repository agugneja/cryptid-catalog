from flask import Flask, render_template, request, abort, redirect
from dotenv import load_dotenv
import os
from datetime import datetime
from src.models import Post, db
from src.repositories.forum_post import forum_post_singleton

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

@app.post('/sightings')
def create_post():
    #add photo later
    title = request.form.get('title')
    creature = request.form.get('creature')
    description = request.form.get('description')
    user_id = 1
    place = "x"
    likes = 0
    dislikes = 0

    dt = datetime.now()

    if not title or not creature or not description:
        abort(400)

    created_post = forum_post_singleton.create_post(title, creature, dt, user_id, place, 
        description, likes, dislikes)

    return render_template('sightings.html')

@app.get('/logout')
def logout():
    return render_template('login.html')