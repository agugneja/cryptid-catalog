from src.models import Comment, db, commentlikes, commentdislikes
from src.repositories.comment_likes_repository import commentlike_repository_singleton

class CommentRepository:

    #create comment
    def create_comment(self, post_id, text, user_id, time_stamp):
        new_comment = Comment(post_id, text, user_id, time_stamp, likes=0, dislikes=0)
        db.session.add(new_comment)
        db.session.commit()
        return post_id


    #read comment
    def get_comments(self, _post_id):
        return Comment.query.filter_by(post_id=_post_id).order_by(Comment.likes.desc()).all()

    #def has_liked_comment(self, comment_id_, user_id_):
     #   likes =  commentlikes.query.filter_by(comment_id = comment_id_).all()
      #  for like in likes:
       #     if like.user_id == user_id_:
        #        return True
        #return False

    def get_comment_by_id(self, comment_id):
        comment_by_id = Comment.query.filter_by(comment_id=comment_id).first()
        return comment_by_id

    def edit_comment(self, comment_id, text):
        comment = Comment.query.filter_by(comment_id=comment_id).first()
        comment.text = text 
        db.session.commit()
    
    #update comment
    def add_comment_like(self, comment_id, user_id):
        comment =  Comment.query.get(comment_id)
        if commentlike_repository_singleton.has_disliked_comment(comment_id, user_id):
            commentdislikes.query.filter_by(comment_id=comment_id).delete()
            comment.dislikes = comment.dislikes - 1
            new_like = commentlikes(comment_id, user_id)
            db.session.add(new_like)
            comment.likes = comment.likes + 1

        elif commentlike_repository_singleton.has_liked_comment(comment_id, user_id):

            commentlikes.query.filter_by(comment_id=comment_id).delete()
            comment.likes = comment.likes - 1
        else:
            new_like = commentlikes(comment_id, user_id)
            db.session.add(new_like)
            comment.likes = comment.likes + 1
        db.session.commit()

        return None

    def add_comment_dislike(self, comment_id, user_id):
        comment =  Comment.query.get(comment_id)
        if commentlike_repository_singleton.has_liked_comment(comment_id, user_id):
            commentlikes.query.filter_by(comment_id=comment_id).delete()
            comment.likes = comment.likes - 1
            new_dislike = commentdislikes(comment_id, user_id)
            db.session.add(new_dislike)
            comment.dislikes = comment.dislikes + 1

        elif commentlike_repository_singleton.has_disliked_comment(comment_id, user_id):
            commentdislikes.query.filter_by(comment_id=comment_id).delete()
            comment.dislikes = comment.dislikes - 1
        else:
            new_dislike = commentdislikes(comment_id, user_id)
            db.session.add(new_dislike)
            comment.dislikes = comment.dislikes + 1
        db.session.commit()
        return None
    

    #delete comment
    def delete_comment(self, comment_id):
        comment_to_delete = Comment.query.get(comment_id)
        db.session.delete(comment_to_delete)
        db.session.commit()
        return None




comment_repository_singleton = CommentRepository()