from src.models import Post, db
from flask import request

class Post:
    def create_post(self, title, creature, datetime, place, description, photo, likes, dislikes):
        post = Post(title, creature, datetime, place, description, photo, likes, dislikes)
        db.session.add(post)
        db.session.commit()
        return post

forum_post_singleton = Post()
