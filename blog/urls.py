from django.urls import path
from .views import (BloglistView,
                    BlogDetailView,
                    update_post_view,
                    DeletePostView,
                    post_action_get_view,
                    create_comment
                    )



app_name = 'blog'
urlpatterns = [
    path('', BloglistView.as_view(), name='blog_list'),
    path('<str:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<str:slug>/like_action/', post_action_get_view, name='post_action'),
    path('<str:slug>/create_comment/', create_comment, name='blog_comment'),
    path('<str:slug>/update/', update_post_view, name='update_post'),
    path('<str:slug>/delete/', DeletePostView.as_view(), name='delete_post'),



]
# pattern(s)
# tried: ['blog/(?P<slug>[^/]+)/comment/$']