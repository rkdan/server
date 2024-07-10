from django.urls import path
from core.views import MainView, TestTask, WebSocketTest


urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("task/", TestTask.as_view(), name="test_task"),
    path("socket/", WebSocketTest.as_view(), name="web_socket"),
]