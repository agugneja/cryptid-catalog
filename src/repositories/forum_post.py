from src.models import Post, db

class Post:
    #add photo later
    def create_post(self, title, creature, dt, user_id, place, description, likes, dislikes):
        post = Post(title, creature, dt, user_id, place, description, likes, dislikes)
        db.session.add(post)
        db.session.commit()
        return post

forum_post_singleton = Post()
