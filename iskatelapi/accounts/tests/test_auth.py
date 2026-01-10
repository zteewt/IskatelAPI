import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_register_redirects_and_logs_in(api_client):
    resp = api_client.post(
        "/api/auth/register/",
        data={"username": "newuser", "password": "pass12345"},
        format="json",
        follow=False,
    )
    assert resp.status_code in (302, 201)
    assert User.objects.filter(username="newuser").exists()

    points_resp = api_client.get("/api/points/")
    assert points_resp.status_code == 200


@pytest.mark.django_db
def test_login_allows_access_points(api_client, user):
    ok = api_client.login(username="u1", password="pass12345")
    assert ok is True

    resp = api_client.get("/api/points/")
    assert resp.status_code == 200
