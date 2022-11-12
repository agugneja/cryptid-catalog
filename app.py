from flask import Flask, render_template, request, abort, redirect
from dotenv import load_dotenv
from src.models import db
from src.repositories.comment_repository import comment_repository_singleton
import os
from src.models import db

from src.repositories.post_repository import post_repository_singleton

load_dotenv()

app = Flask(__name__)
order_dict = {}

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

db.init_app(app)

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

@app.get('/posts/<int:post_id>')
def get_single_post(post_id):
    single_post = post_repository_singleton.get_post_by_id(post_id)
    ## all_comments = comment_repository_singleton.get_comments()
    return render_template('single_post_page.html', post = single_post) #, comments = all_comments)

@app.get('/comment/<int:post_id>')
def make_commment(post_id):
    return render_template('make_comments.html', post_id = post_id)
