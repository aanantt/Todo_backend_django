from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
# https://www.youtube.com/watch?v=9AECqoFmtJg

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="related_user")
    work = models.CharField(max_length=255)
    isdone = models.BooleanField(default=False)
