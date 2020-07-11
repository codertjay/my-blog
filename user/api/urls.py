from django.urls import path
from .views import (
    UserCreateApiView,
    UserLoginAPIView
)

app_name = 'user_api'
urlpatterns = [
    path('register/', UserCreateApiView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(),name='login'),
    # path('<str:slug>/delete/', PostDeleteApiView.as_view(), name='delete'),
    # path('<str:slug>/update/', PostUpdateApiView.as_view(), name='update'),

]
