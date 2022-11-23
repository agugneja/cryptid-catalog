from flask import Flask, render_template, request, abort, redirect
from dotenv import load_dotenv
from src.models import db
from src.repositories.comment_repository import comment_repository_singleton
from src.repositories.person_repository import person_repository_singleton
from src.repositories.post_repository import post_repository_singleton
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from src.models import Post, db
from src.repositories.forum_post import forum_post_singleton


load_dotenv()

app = Flask(__name__)

order_dict = {}

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.get('/profile/<int:user_id>')
def profile(user_id):
    displayed_user = person_repository_singleton.get_person_by_id(user_id)
    return render_template('profile.html', user_id = displayed_user)

@app.get('/encyclopedia')
def encyclopedia():
    return render_template('encyclopedia.html')

@app.get('/sightings')
def sightings():
    return render_template('sightings.html')


@app.get('/register')
def register():
    return render_template('register.html')

@app.post('/sightings')
def create_post():
    title = request.form.get('title')
    creature = request.form.get('creature')
    description = request.form.get('description')
    user_id = 1
    place = "x"
    likes = 0
    dislikes = 0

    dt = datetime.now()
    # picture validation and functionality
    if 'picture' not in request.files:
        print("not in files")
        abort(400)

    sighting_picture = request.files['picture']

    if sighting_picture.filename == '':
        print("no file name")
        abort(400)

    if sighting_picture.filename.rsplit('.', 1)[1].lower() not in ['jpg', 'jpeg', 'gif', 'png']:
        print(sighting_picture.filename.rsplit('.', 1)[1].lower())
        abort(400)

    safe_filename = secure_filename(sighting_picture.filename)

    sighting_picture.save(os.path.join('static', 'forum_post_pictures', safe_filename))

    #form validation
    if not title or not creature or not description:
        print("incorrect form")
        abort(400)

    created_post = forum_post_singleton.create_post(title, creature, dt, user_id, place, \
        description, safe_filename, likes, dislikes)

    

    return render_template('sightings.html')


@app.get('/logout')
def logout():
    return render_template('login.html')

#create a new user
@app.post('/create_account')
def signup():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    email = request.form.get('email', '')
    #check both fields entered
    if username == '' or password == '' or email == '':
        abort(400)
    #check if user exists

    #create user
    created_user = person_repository_singleton.create_user(username, password, email)
    return redirect(f'/profile/{created_user.user_id}')

@app.get('/posts/<int:post_id>')
def get_single_post(post_id):
    single_post = post_repository_singleton.get_post_by_id(post_id)
    all_comments = comment_repository_singleton.get_comments(post_id)
    poster_id = single_post.user_id
    user = person_repository_singleton.get_person_by_id(poster_id)
    return render_template('single_post_page.html', post = single_post, comments = all_comments, user = user)

@app.get('/comment/<int:post_id>')
def make_commment(post_id):
    return render_template('make_comments.html', post_id = post_id)

@app.post('/like/<int:post_id>/<int:comment_id>')
def like_comment(post_id, comment_id):
    comment_repository_singleton.add_comment_like(comment_id)
    return redirect('/posts/'+ str(post_id))

@app.post('/dislike/<int:post_id>/<int:comment_id>')
def dislike_comment(post_id, comment_id):
    comment_repository_singleton.add_comment_dislike(comment_id)
    return redirect('/posts/' + str(post_id))
