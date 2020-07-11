from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from markdown_deux import markdown

from comments.models import Comment
from.utils import get_read_time

blogCategory = (
    ('ED', 'Education'),
    ('EN', 'Entertainment'),
    ('L', 'Lifestyle'),
    ('MT', 'Modern technology')
)


class BlogPostQueryset(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(published_date__lte=now)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQueryset(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey('Post', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='post', blank=True, null=True)
    category = models.CharField(choices=blogCategory, max_length=3, blank=True, null=True)
    view_count = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    unlike = models.IntegerField(default=0)
    user_action = models.ManyToManyField(User, related_name='blog_action', through=Action, blank=True)
    published_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    read_time = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = BlogPostManager()

    class Meta:
        ordering = ['-published_date', '-timestamp']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

    def get_api_url(self):
        return reverse('blog_api:detail', kwargs={'slug': self.slug})


    @property
    def imageURL(self):
        try:
            image = self.image.url
        except:
            image = ''
        return image

    def get_markdown(self):
        description = self.description
        markdown_text = markdown(description)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        """ to get the comments on the comment models
        i have created a models manager"""
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        """
        this is the content type which is used in the form
        :return: the content type of the post :ie , blog | post
        which is the content type of this post
        """
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = f'{slug,qs.first().id}'
        return create_slug(instance,new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    if instance.description:
        html_string = instance.get_markdown()
        read_time = get_read_time(html_string)
        instance.read_time = read_time


pre_save.connect(pre_save_post_receiver,sender=Post)
