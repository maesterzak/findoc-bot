import os

from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse



class WhatsAppWebhookView(APIView):

    def get(self, request):
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
        print(f"WHATSAPP_VERIFY_TOKEN: {WHATSAPP_VERIFY_TOKEN}")
        print(f"Received token: {token}")
        print(f"Received mode: {mode}")
        print(f"Received challenge: {challenge}")
        print(f"{token == WHATSAPP_VERIFY_TOKEN}")
        print(f"{WHATSAPP_VERIFY_TOKEN}")
        if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
            return HttpResponse(
                challenge,
                status=status.HTTP_200_OK,
                content_type="text/plain"
            )

        return HttpResponse(
            {"error": "Invalid verify token"},
            status=status.HTTP_403_FORBIDDEN,
            content_type="text/plain"
        )

    def post(self, request):
        print("WhatsApp message received:")
        print(request.data)

        return HttpResponse({
            "status": "received"
        }, status=status.HTTP_200_OK, content_type="text/plain")
        

