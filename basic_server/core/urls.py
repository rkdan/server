from django.urls import path
from core.views import MainView, TestTask


urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("task/", TestTask.as_view(), name="test_task"),
]