from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'points', views.PointViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
