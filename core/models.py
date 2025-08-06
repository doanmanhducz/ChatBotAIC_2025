from django.db import models
from django.utils.timezone import now

class ChatSession(models.Model):
    session_id = models.CharField(max_length=100)  # dùng session_id từ Django
    created_at = models.DateTimeField(default=now)
    title = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"Session {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class ChatMessage(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10)  # "user" hoặc "bot"
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)
