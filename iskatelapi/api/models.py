#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Point(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название точки", )
    location = models.PointField(geography=True, verbose_name="Координаты точки")
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Messages(models.Model):
    message = models.TextField(verbose_name="Сообщение к точке")
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)