from django.contrib import admin
from django.urls import path
from .views import home_page, login_page, signup_page, logout_view, main_page, chat_page, chat_query, profile_page, books_page, book_detail, chat_page

urlpatterns = [
    path('', home_page, name='home'),
    path('login/', login_page, name='login'),
    path('signup/', signup_page, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('main-page/', main_page, name='main'),
    path('chat-ai/', chat_page, name='chat'),
    path('chat-ai/query/', chat_query, name='query'),
    path('profile/', profile_page, name='profile'),
    path('books/', books_page, name='books'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('chat/', chat_page, name='chat_page'),
]
