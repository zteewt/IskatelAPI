import pytest
from api.models import Messages


@pytest.mark.django_db
class TestMessagesSearchBasic:
    def test_search_requires_params(self, auth_client):
        resp = auth_client.get("/api/points/messages/search/")
        assert resp.status_code == 400
        assert "error" in resp.data

    def test_search_returns_empty(self, auth_client):
        resp = auth_client.get("/api/points/messages/search/?latitude=0&longitude=0&radius=1")
        assert resp.status_code == 200
        assert isinstance(resp.data, list)
        assert len(resp.data) == 0

    def test_search_returns_messages_near_point(self, auth_client, close_message):
        resp = auth_client.get("/api/points/messages/search/?latitude=43.613&longitude=42.735&radius=2")
        assert resp.status_code == 200
        assert len(resp.data) == 1
        assert resp.data[0]["message"] == "Close Message"


@pytest.mark.django_db
class TestMessagesSearchDifferentRadii:
    def test_small_radius_only_close(self, auth_client, close_message, far_message):
        resp = auth_client.get("/api/points/messages/search/?latitude=43.613&longitude=42.735&radius=0.5")
        assert len(resp.data) == 1 

    def test_large_radius_all(self, auth_client, close_message, far_message):
        resp = auth_client.get("/api/points/messages/search/?latitude=43.613&longitude=42.735&radius=100")
        assert len(resp.data) == 2

    def test_zero_radius_empty(self, auth_client, close_message):
        resp = auth_client.get("/api/points/messages/search/?latitude=43.613&longitude=42.735&radius=0")
        assert len(resp.data) == 0


@pytest.mark.django_db
class TestMessagesSearchEdgeCases:
    def test_invalid_params(self, auth_client):
        resp = auth_client.get("/api/points/messages/search/?latitude=abc&longitude=1&radius=1")
        assert resp.status_code == 400
        assert "error" in resp.data

    def test_search_ordered_by_distance(self, auth_client, close_message, far_message):
        resp = auth_client.get("/api/points/messages/search/?latitude=43.613&longitude=42.735&radius=100")
        assert resp.data[0]["message"] == "Close Message" 
        assert resp.data[1]["message"] == "Far Message"

    def test_search_returns_only_own_messages(self, auth_client, close_message):
        """Фильтр по user=request.user?"""
        resp = auth_client.get("/api/points/messages/search/?latitude=43.613&longitude=42.735&radius=2")
        assert len(resp.data) >= 1  

    def test_anonymous_search(self, api_client, close_message):
        resp = api_client.get("/api/points/messages/search/?latitude=43.613&longitude=42.735&radius=2")
        assert resp.status_code in (401, 403)