from flask.testing import FlaskClient
from src.models import Post, Person, db
from src.repositories.person_repository import person_repository_singleton
from tests.utils import refresh_db


def test_create_account(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_user = Person(username="jdoe", password="password", email="jdoe@yahoo.com")
    db.session.add(test_user)
    db.session.commit()
    
    assert test_user.email == "jdoe@yahoo.com"
    assert test_user.password == "password"
    assert test_user.username == "jdoe"

def test_login_account(test_app: FlaskClient):
    test_user = Person(username="jdoe", password="password", email="jdoe@yahoo.com")
    db.session.add(test_user)
    db.session.commit()
    
    #Run action
    res = test_app.post('/login', data={"username": test_user.username, "password": test_user.password}, follow_redirects = True)
    res_profile = test_app.get(f'/profile/{test_user.user_id}')

    #Assert
    assert b'<h1>Hello jdoe</h1>' in res_profile.data

