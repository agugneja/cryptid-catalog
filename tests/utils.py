from src.models import Post, Person, Comment, CommentLikes, db
def refresh_db():
    Post.query.delete()
    Person.query.delete()
    Comment.query.delete()
    #CommentLikes.query.delete()
    db.session.commit()