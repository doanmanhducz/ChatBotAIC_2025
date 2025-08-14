from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),       # Trang home
    path('chat/', views.chat_view, name='chat'),  # Trang chatbot
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/sessions/', views.chat_sessions_api, name='chat_sessions_api'),
    path('api/messages/<int:session_id>/', views.chat_messages_api, name='chat_messages_api'),
    path("api/sessions/<int:session_id>/delete/", views.delete_chat_session_api, name="delete_chat_session_api")
]
