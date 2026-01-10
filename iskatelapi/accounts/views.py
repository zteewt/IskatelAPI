from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        login(request, user)   

        return redirect('/api/points/')
    