from flask.testing import FlaskClient
from src.models import Post, Person, db
from tests.utils import refresh_db

def test_create_account(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_user = Person(username="jdoe", password="password", email="jdoe@yahoo.com")
    db.session.add(test_user)
    db.session.commit()

    # Asserts
    assert test_user.username == "jdoe"
    assert test_user.password == "password"
    assert test_user.email == "jdoe@yahoo.com"


# def test_login_account():
    # pass


def test_session_profile(test_app: FlaskClient):
    pass
