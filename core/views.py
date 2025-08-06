from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import ChatSession, ChatMessage
from django.views.decorators.http import require_GET


def chat_view(request):
    return render(request, "core/index.html")

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")
        session_id = data.get("session_id")  # ✅ lấy session_id từ client

        if session_id:
            try:
                chat_session = ChatSession.objects.get(id=session_id)
            except ChatSession.DoesNotExist:
                # fallback: tạo mới nếu không tìm thấy
                chat_session = ChatSession.objects.create(session_id=request.session.session_key)
        else:
            # ✅ tạo mới nếu chưa có session
            chat_session = ChatSession.objects.create(session_id=request.session.session_key)
            request.session['current_chat_session_id'] = chat_session.id

        # ✅ Đặt title 1 lần duy nhất
        if not chat_session.title and not ChatMessage.objects.filter(chat_session=chat_session).exists():
            chat_session.title = message[:60]
            chat_session.save()

        # Ghi tin nhắn
        ChatMessage.objects.create(chat_session=chat_session, sender="user", message=message)
        reply = f"Bạn vừa nói: '{message}'"
        ChatMessage.objects.create(chat_session=chat_session, sender="bot", message=reply)

        return JsonResponse({
            "reply": reply,
            "session_id": chat_session.id  # Trả về để frontend dùng tiếp
        })
def home_view(request):
    return render(request, 'core/home.html')


@require_GET
def chat_sessions_api(request):
    session_key = request.session.session_key or request.session.save()
    sessions = ChatSession.objects.filter(session_id=session_key).order_by('-created_at')

    data = []
    for s in sessions:
        latest_msg = s.messages.order_by('-timestamp').first()

        # 🔴 Bỏ qua session chưa có tin nhắn
        if not latest_msg:
            continue

        preview = latest_msg.message[:60] + "..." if latest_msg else "Chưa có tin nhắn"
        data.append({
            "id": s.id,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
            "preview": preview
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
