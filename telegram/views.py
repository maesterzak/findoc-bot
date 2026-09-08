import requests

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from docapp.AiServices.ai_analyser import create_problem_solution
from docapp.models import BotUser
from googleconnect.services.google_docs import (
    create_google_document,
    update_google_document
)
from docapp.AiServices.ai_analyser import analyze_message
import json




def get_or_create_telegram_user(message):
    telegram_user = message.get("from", {})

    telegram_id = telegram_user.get("id")
    username = telegram_user.get("username")

    if not telegram_id:
        raise ValueError("Telegram user ID is missing")

    # Store Telegram IDs in this format
    user_id = f"te:{telegram_id}"

    # Check if user already exists
    user = BotUser.objects.filter(
        user_id__contains=[user_id]
    ).first()

    if user:
        return user

    # User does not exist, so create one
    user = BotUser.objects.create(
        user_id=[user_id],
        display_name=username or f"Telegram User {telegram_id}"
    )

    return user


class TelegramWebhookView(APIView):

    def post(self, request):

        print("TELEGRAM PAYLOAD:", request.data)

        message = request.data.get("message", {})

        text = message.get("text")
        chat_id = message.get("chat", {}).get("id")
        photos = message.get("photo")
        telegram_user_id = message["from"]["id"]
        username = message["from"]["username"]

        print("Chat ID:", chat_id)
        print("Message:", text)
        print("Photos:", photos)
        
        bot_user = get_or_create_telegram_user(message)

        print("Telegram ID:", telegram_user_id)
        print("Username:", username)
        print("BotUser:", bot_user)

        foldersList = {
            "coreDoc": "1yj_IXct8wsUz34y1Q5ckSaahQqXb09Cf94AoDHk5b9I",
            "customizationDoc": "16v3Gynmv54gPsHMBMYLWJxYfwwwhXo4PdEcfKL_9i-A",
            "treasuryDoc": "1_B4F59HwFGYiebPk4LcbFW49-Zz2ewcU",
            "uncategorized": "1dmSyAeJymJSL8XF6qFZcQaIPHPgMmqBW"
        }
        reply = ""

        # ==========================
        # PHOTO
        # ==========================
        if photos:

            photo = photos[-1]
            file_id = photo.get("file_id")

            print("Photo File ID:", file_id)

            # reply = (
            #     "📷 Image received successfully!\n\n"
            #     f"File ID: {file_id}"
            # )
            
        
            

        # # ==========================
        # # TEXT
        # # ==========================
        # if text:

        #     if text == "/start":

        #         reply = "Welcome to FinDoc Bot! 👋"

        #     elif text.lower() == "hello":

        #         reply = "Hello! How can I help you?"

        #     else:

        #         result = update_google_document(
        #             document_id=foldersList.get("coreDoc"),
        #             content="\n" + text
        #         )

        #         reply = (
        #             "Document updated successfully!\n\n"
        #             f"{result['url']}"
        #         )

        # # ==========================
        # # UNKNOWN MESSAGE
        # # ==========================
        # if reply == '':

        #     reply = "I received a message, but I don't understand it yet."

        # ==========================
        # SEND REPLY TO TELEGRAM
        # ==========================

        telegram_url = (
            f"https://api.telegram.org/bot"
            f"{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        )
        
        # CALL CLASSIFIER TO CLEANUP REQUEST
        #TODO
        
        #CALL AI TO ANALYZE MESSAGE
        if text:
            
            reply = analyze_message(text)
            reply = json.loads(reply)
            print("AI REPLY:", reply)
            
            if reply["type"] == "conversation":
                reply = reply["response"]

            elif reply["type"] == "question":
                reply = reply["response"]

            elif reply["type"] == "out_of_scope":
                reply = reply["response"]
            elif reply["type"] == "issue":
                print("ISSUE REPORTED:", reply)
                problem = create_problem_solution(
                    message=text,
                    user_id=telegram_user_id,
                    ai_response=reply,
                )
                
                if problem:
                    reply = (
                    f"✅ Problem documented.\n\n"
                    f"Title: {problem.title}\n"
                    f"ID: {problem.id}"
                    )

        requests.post(
            telegram_url,
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

        return Response({"status": "received"})