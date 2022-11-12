from src.repositories.post_repository import PostRepository
from app import app, movie_repository
import pytest
from src.models import Post

@pytest.fixture()
def test_app():
  return app.test_client()

def test_single_post(test_app):
    TODO