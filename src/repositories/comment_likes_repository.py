from src.models import db, commentlikes, Comment, commentdislikes

class CommentlikesRepository:

    
    def has_liked_comment(self, comment_id_, user_id_):
        likes =  commentlikes.query.filter_by(comment_id = comment_id_).all()
        for like in likes:
            if like.user_id == user_id_:
                return True
        return False

    def get_liked_comment(self, comment_id_):
        liked =  commentlikes.query.filter_by(comment_id = comment_id_).all()
        return liked

   
   
    def has_disliked_comment(self, comment_id_, user_id_):
        likes =  commentdislikes.query.filter_by(comment_id = comment_id_).all()
        for like in likes:
            if like.user_id == user_id_:
                return True
        return False

    def get_disliked_comment(self, comment_id_):
        disliked =  commentdislikes.query.filter_by(comment_id = comment_id_).all()
        return disliked

commentlike_repository_singleton = CommentlikesRepository()