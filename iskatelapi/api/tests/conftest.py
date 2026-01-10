import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


# ----------------------------
# Clients (НЕ шарим состояние)
# ----------------------------

@pytest.fixture
def api_client():
    """Анонимный клиент (без логина)."""
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="user1", password="pass123")


@pytest.fixture
def user2(db):
    return User.objects.create_user(username="user2", password="pass123")


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username="admin", password="pass123", email="[email protected]")


@pytest.fixture
def auth_client(user):
    """Клиент, залогиненный под user1."""
    client = APIClient()
    ok = client.login(username=user.username, password="pass123")
    assert ok is True
    return client


@pytest.fixture
def auth_client2(user2):
    """Клиент, залогиненный под user2."""
    client = APIClient()
    ok = client.login(username=user2.username, password="pass123")
    assert ok is True
    return client


@pytest.fixture
def admin_client(admin_user):
    """Клиент, залогиненный под admin."""
    client = APIClient()
    ok = client.login(username=admin_user.username, password="pass123")
    assert ok is True
    return client


# ----------------------------
# Helpers (payloads)
# ----------------------------

def point_payload(title="Test Point", lon=42.7352, lat=43.6130):
    return {
        "title": title,
        "location": {"type": "Point", "coordinates": [lon, lat]},
    }


# ----------------------------
# Points fixtures
# ----------------------------

@pytest.fixture
def point_id(auth_client, db):
    """Создаёт одну точку от user1 и возвращает её id."""
    resp = auth_client.post("/api/points/", data=point_payload(), format="json")
    assert resp.status_code in (200, 201), resp.data
    assert "id" in resp.data, resp.data
    return resp.data["id"]


@pytest.fixture
def close_point_id(auth_client, db):
    """Точка ~100м от базовой координаты (для search)."""
    resp = auth_client.post(
        "/api/points/",
        data=point_payload(title="Close Point", lon=42.7351, lat=43.6131),
        format="json",
    )
    assert resp.status_code in (200, 201), resp.data
    return resp.data["id"]


@pytest.fixture
def far_point_id(auth_client, db):
    """Точка далеко (для search)."""
    resp = auth_client.post(
        "/api/points/",
        data=point_payload(title="Far Point", lon=42.84, lat=43.70),
        format="json",
    )
    assert resp.status_code in (200, 201), resp.data
    return resp.data["id"]


# ----------------------------
# Messages fixtures
# ----------------------------

@pytest.fixture
def message_id(auth_client, point_id, db):
    """Создаёт сообщение для point_id от user1 и возвращает id сообщения."""
    resp = auth_client.post(
        "/api/points/messages/",
        data={"message": "Test message", "point": point_id},
        format="json",
    )
    assert resp.status_code in (200, 201), resp.data
    assert "id" in resp.data, resp.data
    return resp.data["id"]


@pytest.fixture
def close_message_id(auth_client, close_point_id, db):
    """Сообщение рядом с центром поиска."""
    resp = auth_client.post(
        "/api/points/messages/",
        data={"message": "Close Message", "point": close_point_id},
        format="json",
    )
    assert resp.status_code in (200, 201), resp.data
    assert "id" in resp.data, resp.data
    return resp.data["id"]


@pytest.fixture
def far_message_id(auth_client, far_point_id, db):
    """Сообщение далеко от центра поиска."""
    resp = auth_client.post(
        "/api/points/messages/",
        data={"message": "Far Message", "point": far_point_id},
        format="json",
    )
    assert resp.status_code in (200, 201), resp.data
    assert "id" in resp.data, resp.data
    return resp.data["id"]


@pytest.fixture
def point(point_id):
    return point_id

@pytest.fixture
def closepoint(close_point_id):
    return close_point_id

@pytest.fixture
def farpoint(far_point_id):
    return far_point_id

@pytest.fixture
def closemessage(close_message_id):
    return close_message_id

@pytest.fixture
def farmessage(far_message_id):
    return far_message_id


@pytest.fixture
def close_message(close_message_id):
    return close_message_id

@pytest.fixture
def far_message(far_message_id):
    return far_message_id

@pytest.fixture
def close_point(close_point_id):
    return close_point_id

@pytest.fixture
def far_point(far_point_id):
    return far_point_id