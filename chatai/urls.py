from django.contrib import admin
from django.urls import path
from .views import home_page, login_page, signup_page, logout_view, main_page, chat_page, chat_query, profile_page, books_page, book_detail, foro_page, emotional_state, save_emotion, emotion_log, servicio_page, send_message, fetch_messages, user_chat

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
    path('foro/', foro_page, name='foro'),
    path('emotional-state/', emotional_state, name='emotional_state'),
    path('save_emotion/', save_emotion, name='save_emotion'),
    path('emotion_log/', emotion_log, name='emotion_log'),
    path('servicio/', servicio_page, name='servicio_page'),
    path('chat/<int:user_id>/', user_chat, name='user_chat'),
    path('send_message/', send_message, name='send_message'),
    path('fetch_messages/<int:user_id>/', fetch_messages, name='fetch_messages'),
]
