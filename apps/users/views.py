from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from . import models
from . import serializers

class UserListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer