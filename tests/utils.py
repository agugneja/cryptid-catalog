from src.models import Post, Person, Comment, commentlikes, commentdislikes, postlikes, postdislikes, db
def refresh_db():
    Comment.query.delete()
    Post.query.delete()
    Person.query.delete()
    commentlikes.query.delete()
    commentdislikes.query.delete()
    postlikes.query.delete()
    postdislikes.query.delete()
    db.session.commit()