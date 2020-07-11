from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, default='user/profile.jpg')
    email = models.EmailField()

    @property
    def imageURL(self):
        try:
            image = self.image.url
        except:
            image = None
        return image


def post_save_user_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(author=instance,email=instance.email)
    user_profile, created = Profile.objects.get_or_create(author=instance)


post_save.connect(post_save_user_profile_create, sender=settings.AUTH_USER_MODEL)
