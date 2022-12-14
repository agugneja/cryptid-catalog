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
    

    res_create = test_app.get(f'/create_account', data = {"username": test_user.username, "password": test_user.password, "email": test_user.email})
    res = test_app.get(f'/profile')
    

    
    assert b'<h1>Hello jdoe</h1>' in res.data


def test_login_account(test_app: FlaskClient):
    pass
    

def test_session_profile(test_app: FlaskClient):
    pass
