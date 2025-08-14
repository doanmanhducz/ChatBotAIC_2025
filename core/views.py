from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import ChatSession, ChatMessage
from django.views.decorators.http import require_GET
import os
import requests
from django.views.decorators.http import require_http_methods

API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_reply(message):

    # prompt = [
    #     {"role": "system", "content": "Bạn là ChatGPT-5."},
    #     {"role": "user", "content": input}
    # ]    
    response = query({
    "messages": message,
    "model": "Qwen/Qwen2.5-7B-Instruct:together"
})
    return response["choices"][0]["message"]["content"]


def chat_view(request):
    return render(request, "core/index.html")

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")
        session_id = data.get("session_id")

        if session_id:
            try:
                chat_session = ChatSession.objects.get(id=session_id)
            except ChatSession.DoesNotExist:
                chat_session = ChatSession.objects.create(session_id=request.session.session_key)
        else:
            chat_session = ChatSession.objects.create(session_id=request.session.session_key)
            request.session['current_chat_session_id'] = chat_session.id

        # ✅ Chỉ đặt title nếu chưa có title (lần đầu tiên)
        if not chat_session.title:
            chat_session.title = message[:60]  # dùng nguyên câu hỏi đầu tiên của user
            chat_session.save()
        
        # Ghi tin nhắn người dùng
        ChatMessage.objects.create(chat_session=chat_session, sender="user", message=message)

        # Bot trả lời
        # reply = f"Bạn vừa nói: '{message}'"
        history = [{"role": "system", "content": "Bạn là ChatGPT-5."}]
        messages = chat_session.messages.order_by("timestamp")
        for m in messages:
            history.append({
                "role": "user" if m.sender == "user" else "assistant",
                "content": m.message
            })
        reply = generate_reply(history)
        ChatMessage.objects.create(chat_session=chat_session, sender="bot", message=reply)

        return JsonResponse({
            "reply": reply,
            "session_id": chat_session.id
        })
def home_view(request):
    return render(request, 'core/home.html')


@require_GET
def chat_sessions_api(request):
    session_key = request.session.session_key or request.session.save()
    sessions = ChatSession.objects.filter(session_id=session_key).order_by('-created_at')

    data = []
    for s in sessions:
        if not s.messages.exists():
            continue

        data.append({
            "id": s.id,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
            "title": s.title if s.title else "Chưa có tiêu đề",
            "preview": s.title if s.title else "Chưa có tiêu đề"  # ✅ Giữ key preview để JS cũ vẫn dùng được
        })

    return JsonResponse({"sessions": data})


@require_GET
def chat_messages_api(request, session_id):
    try:
        session = ChatSession.objects.get(id=session_id, session_id=request.session.session_key)
        messages = session.messages.order_by('timestamp').values('sender', 'message', 'timestamp')
        return JsonResponse({"messages": list(messages)})
    except ChatSession.DoesNotExist:
        return JsonResponse({"error": "Không tìm thấy phiên"}, status=404)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_chat_session_api(request, session_id):
    try:
        session = ChatSession.objects.get(id=session_id, session_id=request.session.session_key)
        session.delete()
        return JsonResponse({"success": True})
    except ChatSession.DoesNotExist:
        return JsonResponse({"error": "Không tìm thấy phiên"}, status=404)