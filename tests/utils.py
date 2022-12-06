from src.models import Post, Person, Comment, CommentLikes, db
def refresh_db():
    Comment.query.delete()
    Post.query.delete()
    Person.query.delete()
    #CommentLikes.query.delete()
    db.session.commit()