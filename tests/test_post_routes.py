from flask.testing import FlaskClient
from src.models import Post, Person, db
from tests.utils import refresh_db
def test_get_all_movies(test_app: FlaskClient):
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
    res = test_app.get('/sightings')
    page_data = res.data.decode()

    # Asserts
    assert res.status_code == 200
    assert f'<center><h3>Creature: Loch Ness Monster</h3></center>'
    assert f'<center><p class="mx-5 px-5">Saw the Loch Ness monster. Maybe.</p></center>'