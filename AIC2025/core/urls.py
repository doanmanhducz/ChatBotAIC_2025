from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),       # Trang home
    path('chat/', views.chat_view, name='chat'),  # Trang chatbot
    path('api/chat/', views.chat_api, name='chat_api'),
]
