import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="u1", password="pass12345")


@pytest.fixture
def user2(db):
    return User.objects.create_user(username="u2", password="pass12345")


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username="admin", password="pass12345", email="[email protected]")


@pytest.fixture
def auth_client(api_client, user):
    api_client.login(username="u1", password="pass12345")
    return api_client


@pytest.fixture
def auth_client2(api_client, user2):
    api_client.login(username="u2", password="pass12345")
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.login(username="admin", password="pass12345")
    return api_client
