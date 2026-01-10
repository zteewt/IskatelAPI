import pytest
from django.contrib.gis.geos import Point as GEOSPoint
from api.models import Point as Point_model


@pytest.mark.django_db
class TestPointsListCreate:
    """03: GET /api/points/ (list) + POST /api/points/ (create)"""

    def test_anonymous_cannot_list(self, api_client):
        resp = api_client.get("/api/points/")
        assert resp.status_code in (401, 403)

    def test_authenticated_can_list(self, auth_client):
        resp = auth_client.get("/api/points/")
        assert resp.status_code == 200
        assert isinstance(resp.data, list)

    def test_authenticated_can_create(self, auth_client):
        resp = auth_client.post(
            "/api/points/",
            data={
                "title": "New Point",
                "location": {"type": "Point", "coordinates": [42.7352, 43.6130]},
            },
            format="json",
        )
        assert resp.status_code in (201, 200)
        assert resp.data["title"] == "New Point"


@pytest.mark.django_db
class TestPointsRetrieveUpdateDestroy:
    """04-06: GET/PATCH/DELETE /api/points/{id}/ + permissions"""

    def test_anonymous_cannot_retrieve(self, api_client, point):
        resp = api_client.get(f"/api/points/{point}/")
        assert resp.status_code in (401, 403)

    def test_owner_can_retrieve(self, auth_client, point):
        resp = auth_client.get(f"/api/points/{point}/")
        assert resp.status_code == 200
        assert resp.data["id"] == point

    def test_owner_can_update(self, auth_client, point):
        resp = auth_client.patch(
            f"/api/points/{point}/",
            data={"title": "Updated Point"},
            format="json",
        )
        assert resp.status_code in (200, 202)
        assert resp.data["title"] == "Updated Point"

    def test_other_user_cannot_update(self, auth_client2, point):
        resp = auth_client2.patch(
            f"/api/points/{point}/",
            data={"title": "Hacked"},
            format="json",
        )
        assert resp.status_code in (403, 404)

    def test_owner_can_delete(self, auth_client, point):
        resp = auth_client.delete(f"/api/points/{point}/")
        assert resp.status_code in (204, 200)

    def test_other_user_cannot_delete(self, auth_client2, point):
        resp = auth_client2.delete(f"/api/points/{point}/")
        assert resp.status_code in (403, 404)

    def test_admin_can_delete_any(self, admin_client, point):
        resp = admin_client.delete(f"/api/points/{point}/")
        assert resp.status_code in (204, 200)


@pytest.mark.django_db
class TestPointsPermissionsEdgeCases:
    """06: edge-cases прав доступа"""
    
    def test_admin_can_list_all(self, admin_client):
        resp = admin_client.get("/api/points/")
        assert resp.status_code == 200

    def test_admin_can_update_any(self, admin_client, point):
        resp = admin_client.patch(f"/api/points/{point}/", data={"title": "Admin updated"})
        assert resp.status_code in (200, 202)
