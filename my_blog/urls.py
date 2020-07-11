from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog.api.views import  PostCreateApiView
from blog.views import BlogCreateView, post_action_get_view, BlogUserListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('comment_thread/', include('comments.urls', namespace='comments')),
    path('api/blog/', include('blog.api.urls', namespace='blog_api')),
    path('api/comments/', include('comments.api.urls', namespace='comments_api')),
    # Todo: path('vlog/', include('vlog.urls', namespace='vlog')) might be api

    #  blog create urls  reason for the slug
    path('blog_new/', BlogCreateView.as_view(), name='blog_create'),

    # blog api create view
    path('blog_create_api/', PostCreateApiView.as_view(), name='update'),

    path('', include('user.urls', namespace='user-page')),
    path('api/user/', include('user.api.urls', namespace='user_api')),
    path('user/<str:username>/', BlogUserListView.as_view(), name='blog_user_list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
