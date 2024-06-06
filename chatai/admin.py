from django.contrib import admin
from .models import User, SiteConfig, Chat, Book, ChatMessage, EmotionLog, Message, FAQ

# Register your models here.
admin.site.register(User)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cover_image', 'book_url')

admin.site.register(SiteConfig)
admin.site.register(Chat)
admin.site.register(Book, BookAdmin)
admin.site.register(ChatMessage)
admin.site.register(EmotionLog)
admin.site.register(Message)
admin.site.register(FAQ)