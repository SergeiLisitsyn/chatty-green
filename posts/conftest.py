# conftest.py
import pytest
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='testpass123')

@pytest.fixture
def test_post(db, test_user):
    return Post.objects.create(
        title='Test Post',
        content='Test Content',
        author=test_user
    )

@pytest.fixture
def create_post():
    def _create_post(**kwargs):
        author = kwargs.pop("author", None)
        if not author:
            author = get_user_model().objects.create_user(
                username="testauthor",
                password="testpass123"
            )
        return Post.objects.create(
            title="Test Post",
            slug="test-post",
            text="Test content",
            author=author,
            **kwargs
        )
    return _create_post