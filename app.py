from flask import Flask, render_template, request, abort, redirect, session
from dotenv import load_dotenv
from src.models import db
from src.repositories.comment_repository import comment_repository_singleton
from src.repositories.person_repository import person_repository_singleton
from src.repositories.post_repository import post_repository_singleton
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from src.models import Post, db
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app)

order_dict = {}

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('APP_SECRET_KEY')
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user'  in session:
        return render_template('home.html')
    return render_template('login.html')

@app.get('/profile')
def profile():
    if 'user' in session:
        user_id = session['user']['user_id']
        displayed_user = person_repository_singleton.get_person_by_id(user_id)
        return render_template('profile.html', user_id = displayed_user)
    return redirect('/login')
    
@app.get('/encyclopedia')
def encyclopedia():
    return render_template('encyclopedia.html')

@app.route('/abominableSnowman')
def abominableSnowman():
    return render_template('/entries/abominableSnowman.html')

@app.route('/bigfoot')
def bigfoot():
    return render_template('/entries/bigfoot.html')

@app.route('/chupacabra')
def chupacabra():
    return render_template('/entries/chupacabra.html')

@app.route('/cookieMonster')
def cookieMonster():
    return render_template('/entries/cookieMonster.html')

@app.route('/lizardMan')
def lizardMan():
    return render_template('/entries/lizardMan.html')

@app.route('/lochNess')
def lochNess():
    return render_template('/entries/lochNess.html')

@app.route('/mamlambo')
def mamlambo():
    return render_template('/entries/mamlambo.html')

@app.route('/megalodon')
def megalodon():
    return render_template('/entries/megalodon.html')

@app.route('/mothman')
def mothman():
    return render_template('/entries/mothman.html')

@app.route('/ningen')
def ningen():
    return render_template('/entries/ningen.html')

@app.get('/sightings')
def sightings():
    post_pool = post_repository_singleton.get_all_posts()
    return render_template('sightings.html', posts=post_pool)


@app.get('/register')
def register():
    return render_template('register.html')

@app.get('/logout')
def logout():
    if 'user' in session:
        session.pop('user')    
    return render_template('login.html')

@app.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    existing_user = person_repository_singleton.get_person_by_username(username)

    if not existing_user:
        return redirect('/')

    if not bcrypt.check_password_hash(existing_user.password, password):
        return redirect('/')
    
    session['user'] = {
        'user_id': existing_user.user_id
    }

    return render_template('home.html')


#create a new user
@app.post('/create_account')
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    #check both fields entered
    if username == '' or password == '' or email == '':
        abort(400)
    #check if user exists
    existing_user = person_repository_singleton.get_person_by_username(username)

    #Salt and hash the password
    hashed_bytes = bcrypt.generate_password_hash(password, 10)
    hashed_password = hashed_bytes.decode('utf-8')

    #create user
    created_user = person_repository_singleton.create_user(username, hashed_password, email)

    session['user'] = {
        'user_id': created_user.user_id
    }

    return redirect(f'/sightings')


@app.post('/create_post')
def create_post():
    if 'user' not in session:
        return redirect('/login')
    title = request.form.get('title')
    creature = request.form.get('creature')
    description = request.form.get('description')
    user_id = session['user']['user_id']
    place = "x"
    likes = 0
    dislikes = 0

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

    created_post = post_repository_singleton.create_post(title, creature, user_id, place, \
        description, safe_filename, likes, dislikes)

    return redirect('/posts/' + str(created_post.post_id))


@app.get('/posts/<int:post_id>')
def get_single_post(post_id):
    single_post = post_repository_singleton.get_post_by_id(post_id)
    if single_post is None:
        return render_template('sightings.html')
    all_comments = comment_repository_singleton.get_comments(post_id)
    poster_id = single_post.user_id
    user = person_repository_singleton.get_person_by_id(poster_id)
    if 'user' in session:
        session_user_id = session['user']['user_id']
    else:
        session_user_id = -1

    return render_template('single_post_page.html', post = single_post, comments = all_comments, user = user, session_user_id = session_user_id)

@app.post('/like/<int:post_id>')
def like_post(post_id):
    if 'user' not in session:
        return redirect('/login')
    user_id = session['user']['user_id']
    post_repository_singleton.add_post_like(post_id, user_id)
    return redirect('/posts/'+ str(post_id))

@app.post('/dislike/<int:post_id>')
def dislike_post(post_id):
    if 'user' not in session:
        return redirect('/login')
    user_id = session['user']['user_id']
    post_repository_singleton.add_post_dislike(post_id, user_id)
    return redirect('/posts/'+ str(post_id))

@app.post('/comment/<int:post_id>')
def make_commment(post_id):
    if 'user' not in session:
        return redirect('/login')
    text = request.form.get('message')
    dt = datetime.now()
    user_id = session['user']['user_id']
    comment_repository_singleton.create_comment(post_id, text, user_id, dt)
    return redirect('/posts/' + str(post_id))
    
    #return render_template('make_comments.html', post_id = post_id)

@app.post('/like/<int:post_id>/<int:comment_id>')
def like_comment(post_id, comment_id):
    if 'user' not in session:
        return redirect('/login')
    user_id = session['user']['user_id']
    comment_repository_singleton.add_comment_like(comment_id, user_id)
    return redirect('/posts/'+ str(post_id))

@app.post('/dislike/<int:post_id>/<int:comment_id>')
def dislike_comment(post_id, comment_id):
    if 'user' not in session:
        return redirect('/login')
    user_id = session['user']['user_id']
    comment_repository_singleton.add_comment_dislike(comment_id, user_id)
    return redirect('/posts/'+ str(post_id))

#function to get from encyclopedia entry to sightings post
@app.post('/entry_to_post')
def entry_to_post(creature):
    post_pool = post_repository_singleton.get_posts_by_creature(creature)
    return redirect('sightings.html', posts=post_pool)

#function to get from sightings post to encyclopedia entry
@app.post('/post_to_entry')
def post_to_entry():
    entry_page= request.form.get('creature')
    return render_template('entries/' + str(entry_page) + '.html')

#filters all posts by creature, username, or both, or neither
@app.post('/filter_posts')
def filter_posts(creature, username):
    #tests if a user with said username doesn't exist
    if person_repository_singleton.get_person_by_username(username) is None:
        #creature has default 'all' (neither creature or user)
        if creature == 'all':
            post_pool = post_repository_singleton.get_all_posts()
        #creature is not default, so filter by creature (creature only)
        else:
            post_pool = post_repository_singleton.get_posts_by_creature(creature)
    
    #the other option, the user does exist 
    else:
        #gets the user_id since the user exits
        user_id = person_repository_singleton.get_user_id_by_username(username)
        
        #creature is default 'all' (user only)
        if creature == 'all':
            post_pool = post_repository_singleton.get_posts_by_user_id(user_id)
        #creature isn't default, so use both (user and creature))
        else:
            post_pool = post_repository_singleton.get_posts_by_user_and_creature(user_id, creature)
    
    return redirect('sightings.html', posts=post_pool)


#sends user from full sightings page to post creation page
@app.get('/posts_to_creator')
def post_creator():
    return render_template('create_post.html')

#sends user from full sightings page to single post page
@app.get('/posts_to_single_post')
def post_to_post():
    post_id = request.form.get('post_id')
    return redirect('/posts/'+ str(post_id))

@app.post('/edit_post/<int:post_id>')
def edit_post(post_id):
    single_post = post_repository_singleton.get_post_by_id(post_id)
    poster_id = single_post.user_id
    user = person_repository_singleton.get_person_by_id(poster_id)
    poster_id = single_post.user_id
    return render_template('edit_post.html', post = single_post, user = user)

@app.post('/submit_edit/<int:post_id>')
def submit_edit(post_id):
    new_title = request.form.get('edit_title')
    new_creature = request.form.get('edit_creature')
    new_description = request.form.get('edit_description')
    post_repository_singleton.edit_post(post_id, new_title, new_creature, new_description)
    return redirect('/posts/' + str(post_id))

@app.post('/delete_post/<int:post_id>')
def delete_post(post_id):
    post_repository_singleton.delete_post(post_id)
    return render_template('sightings.html')


@app.post('/edit_comment/<int:post_id>/<int:comment_id>')
def edit_comment(post_id, comment_id):

    single_post = post_repository_singleton.get_post_by_id(post_id)
    if single_post is None:
        return render_template('sightings.html')
    all_comments = comment_repository_singleton.get_comments(post_id)
    poster_id = single_post.user_id
    user = person_repository_singleton.get_person_by_id(poster_id)
    if 'user' in session:
        session_user_id = session['user']['user_id']
    else:
        session_user_id = -1

    comment_to_edit = comment_repository_singleton.get_comment_by_id(comment_id)
    return render_template('edit_comment.html', post = single_post, user = user, comments = all_comments, edit_comment = comment_to_edit, session_user_id = session_user_id)




@app.post('/submit_edit_comment/<int:post_id>/<int:comment_id>')
def submit_edit_comment(post_id, comment_id):
    new_comment = request.form.get('new_comment')
    comment_repository_singleton.edit_comment(comment_id, new_comment)
    return redirect('/posts/' + str(post_id))

@app.post('/delete_comment/<int:post_id>/<int:comment_id>')
def delete_comment(post_id, comment_id):
    comment_repository_singleton.delete_comment(comment_id)
    return redirect('/posts/' + str(post_id))

