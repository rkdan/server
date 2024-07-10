from django.urls import path
from core.views import MainView, WebSocket, InferenceAI, HtmxTest


urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("socket/", WebSocket.as_view(), name="web_socket"),
    path("ai/", InferenceAI.as_view(), name="ai"),
    path("htmx_socket/", HtmxTest.as_view(), name="HtmxTest"),
]