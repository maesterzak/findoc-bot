import requests

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from googleconnect.services.google_docs import create_google_document,update_google_document

class TelegramWebhookView(APIView):

    def post(self, request):
        print("TELEGRAM PAYLOAD:", request.data)
        message = request.data.get("message", {})

        text = message.get("text")
        chat_id = message.get("chat", {}).get("id")

        print("Chat ID:", chat_id)
        print("Message:", text)
        
        foldersList = {
        "coreDoc":"1yj_IXct8wsUz34y1Q5ckSaahQqXb09Cf94AoDHk5b9I",
        "customizationDoc":"16v3Gynmv54gPsHMBMYLWJxYfwwwhXo4PdEcfKL_9i-A",
        "treasuryDoc":"1_B4F59HwFGYiebPk4LcbFW49-Zz2ewcU",
        "uncategorized":"1dmSyAeJymJSL8XF6qFZcQaIPHPgMmqBW"
        }

        
        if text == "/start":
            reply = "Welcome to FinDoc Bot! 👋"

        elif text.lower() == "hello":
            reply = "Hello! How can I help you?"

        # else:
        #     result = create_google_document(
        #     "Telegram Test Document",
        #     text
        # )
        else:
            result = update_google_document(
            document_id=foldersList.get("coreDoc"),  # Replace with your actual document ID
            content="\n" + text
        )

        reply = (
            "Document updated successfully!\n\n"
            f"{result['url']}"
        )

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