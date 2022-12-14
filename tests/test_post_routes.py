from flask.testing import FlaskClient
from src.models import Post, Person, Comment, commentlikes, commentdislikes, db
from src.repositories.post_repository import post_repository_singleton
from src.repositories.comment_repository import comment_repository_singleton
from tests.utils import refresh_db
from datetime import datetime

def test_create_post(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_user = Person(username="jdoe", password="password", email="jdoe@yahoo.com")
    db.session.add(test_user)
    db.session.commit()
    test_sighting = Post(title='Monster Sighted', creature='Loch Ness Monster', 
    user_id=test_user.user_id, place='Loch Ness', description='Saw the Loch Ness monster. Maybe.', 
    photo_path='static/forum_post_pictures/placeholder.png', likes='3', dislikes='12')

    db.session.add(test_sighting)
    db.session.commit()

    # Run action
    res = test_app.get(f'/posts/{test_sighting.post_id}')

    # Asserts
    assert test_user.username == "jdoe"
    assert test_user.password == "password"
    assert test_user.email == "jdoe@yahoo.com"

    assert res.status_code == 200
    assert test_sighting.title == "Monster Sighted"
    assert test_sighting.creature == "Loch Ness Monster"
    assert test_sighting.user_id == test_user.user_id
    assert test_sighting.place == "Loch Ness"
    assert test_sighting.description == "Saw the Loch Ness monster. Maybe."
    assert test_sighting.photo_path == "static/forum_post_pictures/placeholder.png"
    assert test_sighting.likes == 3
    assert test_sighting.dislikes == 12

def test_create_comment(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_user = Person(username="jdoe", password="password", email="jdoe@yahoo.com")
    test_commenter = Person(username="MonsterMan", password="123abc", email="asmith@gmail.com")

    db.session.add(test_user)
    db.session.add(test_commenter)
    db.session.commit()

    test_sighting = Post(title='Monster Sighted', creature='Loch Ness Monster', 
    user_id=test_user.user_id, place='Loch Ness', description='Saw the Loch Ness monster. Maybe.', 
    photo_path='static/forum_post_pictures/placeholder.png', likes='3', dislikes='12')

    db.session.add(test_sighting)
    db.session.commit()


    test_comment = Comment(post_id = test_sighting.post_id, text = "Elaborate. Please.", 
    user_id = test_commenter.user_id, time_stamp = datetime.now(), likes = 0, dislikes = 0)

    db.session.add(test_comment)
    db.session.commit()

    # Run action
    res = test_app.post(f'/comment/{test_sighting.post_id}')

    assert test_comment.post_id == test_sighting.post_id
    assert test_comment.text == "Elaborate. Please."
    assert test_comment.user_id == test_commenter.user_id
    assert test_comment.likes == 0
    assert test_comment.dislikes == 0

def test_like_comment(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_user = Person(username="jdoe", password="password", email="jdoe@yahoo.com")
    test_commenter = Person(username="MonsterMan", password="123abc", email="asmith@gmail.com")

    db.session.add(test_user)
    db.session.add(test_commenter)
    db.session.commit()

    test_sighting = Post(title='Monster Sighted', creature='Loch Ness Monster', 
    user_id=test_user.user_id, place='Loch Ness', description='Saw the Loch Ness monster. Maybe.', 
    photo_path='static/forum_post_pictures/placeholder.png', likes='3', dislikes='12')

    db.session.add(test_sighting)
    db.session.commit()


    test_comment = Comment(post_id = test_sighting.post_id, text = "Elaborate. Please.", 
    user_id = test_commenter.user_id, time_stamp = datetime.now(), likes = 0, dislikes = 0)

    db.session.add(test_comment)
    db.session.commit()

    #test_liked = comment_repository_singleton.add_comment_like(test_comment.comment_id, test_user.user_id)
    #db.session.add(test_liked)
    #db.session.commit()

    # Run action
    resComment = test_app.post(f'/comment/{test_sighting.post_id}')
    resLike = test_app.post(f'/like/{test_sighting.post_id}/{test_comment.comment_id}')
    # test_app.post('/login')
    page_data = resLike.data.decode()

    assert test_comment.post_id == test_sighting.post_id
    assert test_comment.text == "Elaborate. Please."
    assert test_comment.user_id == test_commenter.user_id
    assert '<button type="submit" class="btn btn-success">&#8205; &#8205; &#8205; LIKE &#8205; &#8205; &#8205; </button> &#8205 1' in page_data
    assert test_comment.dislikes == 0

# def test_dislike_comment(test_app: FlaskClient):
#     pass

# def test_edit_post(test_app: FlaskClient):
#     # Setup
#     refresh_db()
#     test_user = Person(username="jdoe", password="password", email="jdoe@yahoo.com")
#     db.session.add(test_user)
#     db.session.commit()
#     test_sighting = Post(title='Monster Sighted', creature='Loch Ness Monster', 
#     user_id=test_user.user_id, place='Loch Ness', description='Saw the Loch Ness monster. Maybe.', 
#     photo_path='static/forum_post_pictures/placeholder.png', likes='3', dislikes='12')

#     db.session.add(test_sighting)
#     db.session.commit()

#     test_sighting = post_repository_singleton.edit_post(test_sighting.post_id, "Monster Sighted",
#     "Loch Ness Monster", "Saw a creature at Loch Ness that matches the supposed \
#     description for the Loch Ness Monster.")

#     db.session.add(test_sighting)
#     db.session.commit()


#This needs to also call edit_post
#     # Run action
#     test_app.get(f'/submit_edit/{test_sighting}')

#     # Asserts
#     assert test_sighting.title == "Monster Sighted"
#     assert test_sighting.creature == "Loch Ness Monster"
#     assert test_sighting.description == "Saw a creature at Loch Ness that matches the supposed \
#     description for the Loch Ness Monster."

def test_delete_post(test_app: FlaskClient):
    pass

def test_edit_comment(test_app: FlaskClient):
    pass

#def test_delete_comment(test_app: FlaskClient):
#    pass

