from src.models import Post, db

class PostRepository:
    #add photo later
    def create_post(self, title, creature, dt, user_id, place, description, picture, likes, dislikes):
        post = Post(title, creature, dt, user_id, place, description, picture, likes, dislikes)
        db.session.add(post)
        db.session.commit()
        return post

forum_post_singleton = PostRepository()
