from src.models import Comment, db

class CommentRepository:

    #create comment
    def create_comment(self, post_id, text, user_id, time_stamp):
        new_comment = Comment(post_id=post_id, text=text, \
             user_id=user_id, time_stamp=time_stamp, likes=0, dislikes=0)
        db.session.add(new_comment)
        db.session.commit()
        return post_id

    #read comment
    def get_comments(self, _post_id):
        return Comment.query.filter_by(post_id=_post_id).order_by(Comment.likes.desc()).all()

    
    #update comment
    def add_comment_like(self, comment_id):
        comment =  Comment.query.get(comment_id)
        comment.likes = comment.likes + 1
        db.session.commit()
        return None
    
    def add_comment_dislike(self, comment_id):
        comment =  Comment.query.get(comment_id)
        comment.dislikes = comment.dislikes + 1
        db.session.commit()
        return None

    #delete comment
    def remove_comment(self, comment_id):
        comment_to_delete =  Comment.query.get(comment_id)
        db.session.delete(comment_to_delete)
        db.session.commmit()
        return None

comment_repository_singleton = CommentRepository()