from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)

    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'Person(user_id={self.user_id}, username={self.username}, password={self.password})'

class Post(db.Model):
    #add photo later
    post_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    creature = db.Column(db.String, nullable = False)
    date_time = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('person.user_id'), nullable = False)
    user = db.relationship('Person', backref='users', primaryjoin='Post.user_id == Person.user_id')
    place = db.Column(db.String, nullable = False)
    description = db.Column(db.Text, nullable = False)
    likes = db.Column(db.Integer, nullable = False)
    dislikes = db.Column(db.Integer, nullable = False)

    def __init__(self, title:str, creature:str, date_time:int, user_id:int, place: str, description:str, likes:int, dislikes:int):
        self.title = title
        self.creature = creature
        self.date_time = date_time
        self.user_id = user_id
        self.place = place
        self.description = description
        self.likes = likes
        self.dislikes = dislikes

    def __repr__(self) -> str:
        return f'Post(post_id={self.post_id}, title={self.title}, creature={self.creature}, date_time={self.date_time}, user_id={self.user_id}, place={self.place}, description={self.description}, likes={self.likes}, dislikes={self.dislikes})'

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, nullable = False)
    text = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, nullable = False)
    time_stamp = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)
    dislikes = db.Column(db.Integer, nullable = False)

    def __init__(self, post_id:int, text:str, user_id:str, time_stamp:int, likes:int, dislikes:int):
        self.post_id = post_id
        self.text = text
        self.user_id = user_id
        self.time_stamp = time_stamp
        self.likes = likes
        self.dislikes = dislikes

    def __repr__(self) -> str:
        return f'Comment(comment_id={self.comment_id}, text={self.text}, user_id={self.user_id}, time_stamp={self.time_stamp}, likes={self.likes}, dislikes={self.dislikes})'