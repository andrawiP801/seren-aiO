from django.contrib import admin
from .models import User, SiteConfig, Chat, Book, ChatMessage, EmotionLog

# Register your models here.
admin.site.register(User)

admin.site.register(SiteConfig)
admin.site.register(Chat)
admin.site.register(Book)
admin.site.register(ChatMessage)
admin.site.register(EmotionLog)