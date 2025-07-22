from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def chat_view(request):
    return render(request, "core/index.html")

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")

        # Trả lời giả lập - sau này tích hợp AI model tại đây
        reply = f"Bạn vừa nói: '{message}'"

        return JsonResponse({"reply": reply})
