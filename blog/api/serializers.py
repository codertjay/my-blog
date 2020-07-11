from dataclasses import fields

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from blog.models import Post
from comments.api.serializers import CommentListSerializer
from comments.models import Comment
from user.api.serializers import UserDetailSerializer

""" we are using the namespace of the app and the then the name space of the 
delete url """


# blog_delete_url = HyperlinkedIdentityField(
#     view_name='blog_api:delete',
#     lookup_field='slug'
# )

class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='blog_api:detail',
        lookup_field='slug'
    )
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'user',
            'url',
            'slug',
            'title',
            'category',
            'timestamp',
        ]


class PostDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'slug',
            'user',
            'title',
            'image',
            'description',
            'html',
            'category',
            'timestamp',
            'comments',
        ]

    def get_image (self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_html (self, obj):
        return str(obj.get_markdown())

    def get_comments (self, obj):
        """this filter_by_instance and get_content_type was defined in our models
          note you have to serialize it that is why i use the
          CommentSerializer i created for the content_type and the object_id
         """
        # content_type = obj.get_content_type  # not using it
        # object_id = obj.id  # already defined a method for it
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentListSerializer(c_qs, many=True).data
        return comments


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'slug',
            'title',
            'description',
            'category',
            'image',
            'published_date'
        ]
