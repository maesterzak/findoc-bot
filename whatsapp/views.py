from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class WhatsAppWebhookView(APIView):

    def get(self, request):
        return Response({
            "message": "WhatsApp webhook is working"
        })

    def post(self, request):
        print("WhatsApp message received:")
        print(request.data)

        return Response({
            "status": "received"
        }, status=status.HTTP_200_OK)