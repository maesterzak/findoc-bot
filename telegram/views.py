import requests

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


class TelegramWebhookView(APIView):

    def post(self, request):

        message = request.data.get("message", {})

        text = message.get("text")
        chat_id = message.get("chat", {}).get("id")

        print("Chat ID:", chat_id)
        print("Message:", text)
        
        if text == "/start":
            reply = "Welcome to FinDoc Bot! 👋"

        elif text.lower() == "hello":
            reply = "Hello! How can I help you?"

        else:
            reply = f"I received: {text}"

        # Send reply back to Telegram
        telegram_url = (
            f"https://api.telegram.org/bot"
            f"{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        )

        requests.post(
            telegram_url,
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

        return Response({"status": "received"})