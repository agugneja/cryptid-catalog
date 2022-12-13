from src.models import db, postlikes, Post, postdislikes

class PostlikesRepository:

    
    def has_liked_post(self, post_id_, user_id_):
        likes =  postlikes.query.filter_by(post_id = post_id_).all()
        for like in likes:
            if like.user_id == user_id_:
                return True
        return False

    def get_liked_post(self, post_id_):
        liked =  postlikes.query.filter_by(post_id = post_id_).all()
        return liked

   
    def has_disliked_post(self, post_id, user_id_):
        dislikes =  postdislikes.query.filter_by(post_id = post_id).all()
        for dislike in dislikes:
            if dislike.user_id == user_id_:
                return True
        return False

    def get_disliked_post(self, post_id):
        disliked =  postdislikes.query.filter_by(post_id = post_id).all()
        return disliked

postlike_repository_singleton = PostlikesRepository()