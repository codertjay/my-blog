from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response

#  my own
from .serializers import (
    UserCreateSerializer, UserLoginSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]




class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)  # rest api response
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# class UserUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]
#     serializer_class = UserCreateSerializer
