from src.models import Post, Person, Comment, commentlikes, db
def refresh_db():
    Comment.query.delete()
    Post.query.delete()
    Person.query.delete()
    commentlikes.query.delete()
    db.session.commit()