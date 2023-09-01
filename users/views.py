from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from users.models import CustomUser
from users.pagination import UsersPagination
from users.serializers import CustomUserSerializer


# Create your views here.
class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = UsersPagination
