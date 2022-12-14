from src.models import Post, Person, Comment, commentlikes, commentdislikes, postlikes, postdislikes, db
from src.models import Post, Person, Comment, commentlikes, db
def refresh_db():
    commentlikes.query.delete()
    commentdislikes.query.delete()
    Comment.query.delete()
    postlikes.query.delete()
    postdislikes.query.delete()
    Post.query.delete()
    Person.query.delete()
    db.session.commit()