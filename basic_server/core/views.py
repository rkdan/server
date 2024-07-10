from django.http import JsonResponse, HttpResponse
from django.views import View
from core.tasks import add
from django.shortcuts import render

class MainView(View):
    def get(self, request, *args, **kwargs):
        html_content = "<html><body><h1>Hello, Crocodile 🐊</h1></body></html>"
        return HttpResponse(html_content, content_type="text/html; charset=utf-8")

class TestTask(View):
  def get(self, request, *args, **kwargs):
     try:
         params = { #EXAMPLE ARGS
             'x':11,
             'y':5
         }
         task = add.delay(params)  # RUN THE TASK 
         return JsonResponse({'data': 'initialising', 'task_id': task.id}, status=200)     
     except Exception as e:
         return JsonResponse({'error': str(e)}, status=401) 