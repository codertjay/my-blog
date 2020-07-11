from django.urls import path

from .views import (
    CommentDetailAPIView,
    CommentListApiView,
    CommentCreateApiView,
)
app_name = 'comments_api'
urlpatterns = [
    path('', CommentListApiView.as_view(), name='list'),
    path('create/', CommentCreateApiView.as_view(), name='create'),
    path('<int:id>/', CommentDetailAPIView.as_view(), name='thread'),
]

