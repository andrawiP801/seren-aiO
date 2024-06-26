import uuid
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .storages import OverwriteStorage



class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.username


User.groups.field.remote_field.related_name = "custom_user_groups"
User.user_permissions.field.remote_field.related_name = "custom_user_permissions"


# site config
class SiteConfig(models.Model):
    open_ai_key = models.CharField(max_length=1000)
    open_ai_model = models.CharField(max_length=1000, blank=True, null=True)
    prompt = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.open_ai_model


# chat model
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_message = models.TextField(blank=True, null=True)
    ai_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default="Unknown")
    description = models.TextField()
    cover_image = models.CharField(max_length=200, null=True, blank=True)  # Nombre del archivo de la portada
    book_url = models.URLField(max_length=200, null=True, blank=True)  # URL del libro

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}'
  
    
class EmotionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.emotion} - {self.date}"
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question