from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from rest_framework.authtoken.models import Token
# from django.utils.translation import gettext as _
#from core.models import Item


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.username)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ManyToManyField('core.Item', blank=True)

    def __str__(self):
        return self.user.username


def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        # token = Token.objects.create(user=instance)
        # print(token.key)

post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)