from django.urls import path
from .views import TelegramWebhookView, WhatsAppWebhookView

urlpatterns = [
    path('webhook/', WhatsAppWebhookView.as_view()),
    path('telegram/webhook/', TelegramWebhookView.as_view()),
]