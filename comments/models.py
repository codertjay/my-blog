from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

"""
this is my comments models manager
"""


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)  # which is the post
        obj_id = instance.id  # this is the post.id or any model.id understand
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            """ is just like we are getting the first post which is like a detail 
             of the post """
            my_qs = SomeModel.objects.filter(slug=slug).first()
            obj_qs = my_qs
            if obj_qs:  # checkin  if the queryset exist
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.id
                if parent_obj:
                    print(instance)
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """
    below are the three generic foreignkey which are taking place for post
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse('comments:comment_thread', kwargs={'id': self.id})

    def children(self):
        """ the bottom level this is the reply to the comments so
        we use when looping through the normal comments like a nested comment

         we still use it in our api serializer for the children """
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        """ Note the parent is the first comment created
        if there is no parent it would return false

        note we are using it in our api where we define the replies
        for the children """
        if self.parent is not None:
            return False
        return True
