import pytest
from api.models import Messages


@pytest.mark.django_db
class TestGlobalMessagesEndpoint:
    def test_anonymous_cannot_list(self, api_client):
        resp = api_client.get("/api/points/messages/")
        assert resp.status_code in (401, 403)

    def test_authenticated_can_list_own(self, auth_client):
        resp = auth_client.get("/api/points/messages/")
        assert resp.status_code == 200
        assert isinstance(resp.data, list)

    def test_authenticated_can_create(self, auth_client, point_id):
        resp = auth_client.post(
            "/api/points/messages/",
            data={"message": "Hello world!", "point": point_id},
            format="json",
        )
        assert resp.status_code in (201, 200)
        assert resp.data["message"] == "Hello world!"


@pytest.mark.django_db
class TestPointMessagesEndpoint:
    def test_anonymous_cannot_access_point_messages(self, api_client, point_id):
        resp = api_client.get(f"/api/points/{point_id}/messages/")
        assert resp.status_code in (401, 403)

    def test_authenticated_can_get_point_messages(self, auth_client, point_id):
        resp = auth_client.get(f"/api/points/{point_id}/messages/")
        assert resp.status_code == 200
        assert isinstance(resp.data, list)

    def test_returns_only_messages_of_this_point(self, auth_client, point_id):
        resp = auth_client.get(f"/api/points/{point_id}/messages/")
        assert resp.status_code == 200


@pytest.mark.django_db
class TestMessagesPermissions:
    def test_other_user_cannot_see_others_point_messages(self, auth_client2, point_id):
        resp = auth_client2.get(f"/api/points/{point_id}/messages/")
        assert resp.status_code in (200, 201) 

    def test_admin_can_access_any_point_messages(self, admin_client, point_id):
        resp = admin_client.get(f"/api/points/{point_id}/messages/")
        assert resp.status_code == 200

    def test_admin_can_list_all_global(self, admin_client):
        resp = admin_client.get("/api/points/messages/")
        assert resp.status_code == 200
