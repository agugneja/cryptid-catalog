from src.models import Post, db
from src.repositories.comment_repository import comment_repository_singleton


class PostRepository:
    
    def get_post_by_id(self, _post_id):
        post_by_id = Post.query.filter_by(post_id=_post_id).first()
        return post_by_id
    
    def get_all_posts(self):
        return Post.query.all()
    
    #used to filter sightings posts by creature
    def get_posts_by_creature(self, _creature):
        return Post.query.filter_by(creature=_creature)

    #used to filter sightings posts by user_id
    def get_posts_by_user_id(self, _user_id):
        return Post.query.filter_by(user_id=_user_id)

    #used to filter sightings posts by both user_id and creature
    def get_posts_by_user_and_creature(self, _user_id, _creature):
        return Post.query.filter_by(user_id=_user_id).filter_by(creature=_creature)
        

    #add photo later
    def create_post(self, title, creature, dt, user_id, place, description, picture, likes, dislikes):
        post = Post(title, creature, dt, user_id, place, description, picture, likes, dislikes)
        db.session.add(post)
        db.session.commit()
        return post

    def create_post(self, title, creature, user_id, place, description, picture, likes, dislikes):
        post = Post(title, creature, user_id, place, description, picture, likes, dislikes)
        db.session.add(post)
        db.session.commit()
        return post
    
    def edit_post(self, _post_id, title, creature, description):
        post = Post.query.filter_by(post_id=_post_id).first()
        post.title = title
        post.creature = creature
        post.description = description
        db.session.commit()

    def delete_post(self, post_id):
        post_to_delete = Post.query.get(post_id)
        comments_to_delete = comment_repository_singleton.get_comments(post_id)
        for comment in comments_to_delete:
            db.session.delete(comment)
        db.session.delete(post_to_delete)
        db.session.commit()
        return None

# Singleton to be used in other modules
post_repository_singleton = PostRepository()
