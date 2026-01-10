import pytest
from django.contrib.gis.geos import Point
from api.models import Point as Point_model  


@pytest.mark.django_db
class TestPointsSearchBasic:

    def test_search_requires_params(self, auth_client):
        resp = auth_client.get("/api/points/search/")
        assert resp.status_code == 400
        assert "error" in resp.data

    def test_search_returns_empty_with_valid_params(self, auth_client):
        resp = auth_client.get("/api/points/search/?latitude=0&longitude=0&radius=1")
        assert resp.status_code == 200
        assert isinstance(resp.data, list)
        assert len(resp.data) == 0

    def test_search_returns_points_in_radius(self, auth_client, close_point):
        resp = auth_client.get("/api/points/search/?latitude=43.613&longitude=42.735&radius=2")
        assert resp.status_code == 200
        assert len(resp.data) == 1
        assert resp.data[0]["title"] == "Close Point"


@pytest.mark.django_db
class TestPointsSearchDifferentRadii:
    def test_small_radius_excludes_far_points(self, auth_client, close_point, far_point):
        """R=0.5km → только близкая"""
        resp = auth_client.get("/api/points/search/?latitude=43.613&longitude=42.735&radius=0.5")
        assert len(resp.data) == 1 

    def test_large_radius_includes_all(self, auth_client, close_point, far_point):
        """R=100km → все точки"""
        resp = auth_client.get("/api/points/search/?latitude=43.613&longitude=42.735&radius=100")
        assert len(resp.data) == 2

    def test_zero_radius_returns_empty(self, auth_client, close_point):
        resp = auth_client.get("/api/points/search/?latitude=43.613&longitude=42.735&radius=0")
        assert len(resp.data) == 0


@pytest.mark.django_db
class TestPointsSearchEdgeCases:
    def test_invalid_params_returns_error(self, auth_client):
        resp = auth_client.get("/api/points/search/?latitude=abc&longitude=1&radius=1")
        assert resp.status_code == 400
        assert "error" in resp.data

    def test_search_ordered_by_distance(self, auth_client, close_point, far_point):
        resp = auth_client.get("/api/points/search/?latitude=43.613&longitude=42.735&radius=100")
        assert resp.data[0]["title"] == "Close Point"
        assert resp.data[1]["title"] == "Far Point"

    def test_search_anonymous(self, api_client, close_point):
        resp = api_client.get("/api/points/search/?latitude=43.613&longitude=42.735&radius=2")
        assert resp.status_code in (401, 403)