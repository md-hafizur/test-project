from django.db import models
from django.contrib.auth.models import AbstractUser
from account.user_manager import UserManager
from django.utils import timezone
from utils.token import Token

from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.email

class Session(models.Model):
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    ip = models.GenericIPAddressField()
    user_agent = models.TextField()
    remember = models.BooleanField(default=False)
    access_token_expires = models.DateTimeField(blank=True, null=True)
    refresh_token_expires = models.DateTimeField(blank=True, null=True)

    def update_access_token(self):
        token = Token()
        self.access_token = token.access_token(self.user, expires=5)
        self.access_token_expires = timezone.now() + timezone.timedelta(minutes=5)
        return self.save()

    def update_refresh_token(self):
        token = Token()
        self.refresh_token = token.refresh_token(
            self.user, expires=30 if self.remember else 1
        )
        self.refresh_token_expires = timezone.now() + timezone.timedelta(
            days=30 if self.remember else 1
        )
        return self.save()


@receiver(post_save, sender=Session)
def set_expires(sender, instance, created, **kwargs):
    if created:
        token = Token()
        instance.access_token = token.access_token(instance.user)
        instance.access_token_expires = timezone.now() + timezone.timedelta(minutes=5)
        if instance.remember:
            instance.refresh_token_expires = timezone.now() + timezone.timedelta(
                days=30
            )
            instance.refresh_token = token.refresh_token(instance.user, expires=30)
        else:
            instance.refresh_token_expires = timezone.now() + timezone.timedelta(days=1)
            instance.refresh_token = token.refresh_token(instance.user, expires=1)
        instance.save()
