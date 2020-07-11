from django.urls import path
from .views import (
    PostDetailApiView,
    PostDeleteApiView,
    PostListApiView,
    PostUpdateApiView)


app_name = 'blog_api'
urlpatterns = [
    path('', PostListApiView.as_view(), name='list'),
    path('<str:slug>/', PostDetailApiView.as_view(),name='detail'),
    path('<str:slug>/delete/', PostDeleteApiView.as_view(), name='delete'),
    path('<str:slug>/update/', PostUpdateApiView.as_view(), name='update'),

    # path('<str:slug>/update/', update_post_view, name='update_post'),
    # path('<str:slug>/delete/', DeletePostView.as_view(), name='delete_post')
]
