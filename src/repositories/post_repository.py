from src.models import Post, db, postdislikes, postlikes

from src.repositories.post_likes_repository import postlike_repository_singleton
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
   # def create_post(self, title, creature, dt, user_id, place, description, picture, likes, dislikes):
    #    post = Post(title, creature, dt, user_id, place, description, picture, likes, dislikes)
     #   db.session.add(post)
      #  db.session.commit()
       # return post

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


    def add_post_like(self, post_id, user_id):
        post =  Post.query.get(post_id)
        if postlike_repository_singleton.has_disliked_post(post_id, user_id):
            postdislikes.query.filter_by(post_id=post_id).delete()
            post.dislikes = post.dislikes - 1
            new_like = postlikes(post_id, user_id)
            db.session.add(new_like)
            post.likes = post.likes + 1

        elif postlike_repository_singleton.has_liked_post(post_id, user_id):

            postlikes.query.filter_by(post_id=post_id).delete()
            post.likes = post.likes - 1
        else:
            new_like = postlikes(post_id, user_id)
            db.session.add(new_like)
            post.likes = post.likes + 1
        db.session.commit()

        return None

    def add_post_dislike(self, post_id, user_id):
        post =  Post.query.get(post_id)
        if postlike_repository_singleton.has_liked_post(post_id, user_id):
            postlikes.query.filter_by(post_id=post_id).delete()
            post.likes = post.likes - 1
            new_dislike = postdislikes(post_id, user_id)
            db.session.add(new_dislike)
            post.dislikes = post.dislikes + 1

        elif postlike_repository_singleton.has_disliked_post(post_id, user_id):
            postdislikes.query.filter_by(post_id=post_id).delete()
            post.dislikes = post.dislikes - 1
        else:
            new_dislike = postdislikes(post_id, user_id)
            db.session.add(new_dislike)
            post.dislikes = post.dislikes + 1
        db.session.commit()
        return None

# Singleton to be used in other modules
post_repository_singleton = PostRepository()
