from src.models import db, CommentLikes, Comment

class CommentlikesRepository:

    
    def has_liked_comment(self, comment_id_, user_id_):
        likes =  CommentLikes.query.filter_by(comment_id = comment_id_).all()
        for like in likes:
            if like.user_id == user_id_:
                return True
        return False


commentlike_repository_singleton = CommentlikesRepository()