from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError
)
from comments.models import Comment
from django.contrib.auth import get_user_model
from user.api.serializers import UserDetailSerializer


def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
    User = get_user_model()

    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp',
            ]

        """ in here we are initializing the whole data by using init and getting it from
        the function in which the class is in """

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None

            if parent_id:
                """ what is happenning here is that if the parnet id is being passed 
                then we are going to set it to the create comment serializer """
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        """ in here we are validating the slug and the model type for the content type 
        """

        def validate(self, data):
            model_type = self.model_type
            """below in here we are filtering through the content type to check if the 
            model_type exist which could be Post """
            model_qs = ContentType.objects.filter(model=model_type)
            print("This is  model_qs", model_qs)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError('This is not a valid content type')
            someModel = model_qs.first().model_class()
            """ below is just like we are saying Post.objects.filter(slug=slug)"""
            obj_qs = someModel.objects.filter(slug=self.slug)
            print("This is  obj_qs", obj_qs)
            if not obj_qs or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get('content')
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type=model_type, slug=slug, content=content
                , user=main_user, parent_obj=parent_obj)
            return comment

    return CommentCreateSerializer


class CommentListSerializer(ModelSerializer):
    user = SerializerMethodField()
    try:
        comment_detail_url = HyperlinkedIdentityField(
            view_name='comments_api:thread',
            lookup_field='id',
        )
    except:
        comment_detail_url = None
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'user',
            'id',
            'comment_detail_url',
            'object_id',
            'content_type',
            'parent',
            'content',
            'timestamp',
            'reply_count'
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return None


class CommentChildSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'user',
            'id',
            'content',
            'timestamp',
        ]

    def get_user(self, obj):
        return str(obj.user.username)


class CommentDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    content_absolute_url = SerializerMethodField()

    class Meta:
        model = Comment
        read_only_fields = [
            'reply_count',
            'replies',
        ]
        fields = [
            'user',
            'id',
            'content',
            'content_absolute_url',
            'timestamp',
            'reply_count',
            'replies',
        ]

    def get_content_absolute_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        """ what we are trying to do here is getting the
         children which are the comment replies
         this obj.children() could be anything it could be Comment.objects.all()
         or any models i would like to put there that i want to serialize as
         as i have made the serializer for the file i want to serialize and the
         many=True means it is bring more that one data """
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return None
