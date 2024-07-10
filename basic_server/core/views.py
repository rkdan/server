from django.http import JsonResponse, HttpResponse
from django.views import View
from core.tasks import inference_ai
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.tasks import inference_ai

class MainView(View):
    def get(self, request, *args, **kwargs):
        html_content = "<html><body><h1>Hello, Crocodile 🐊</h1></body></html>"
        return HttpResponse(html_content, content_type="text/html; charset=utf-8")

class InferenceAI(View):
    def get(self, request, *args, **kwargs):
        try:
            task = inference_ai.delay()  # start the celery worker
            return JsonResponse({'data': 'initialising', 'task_id': task.id}, status=200)     
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)   

class WebSocket(View):
    def get(self, request, *args, **kwargs):
      try:
          return render(request, "websocket.html")
      except Exception as e:
          print(str(e))
          return HttpResponse({'error': str(e)}, status=401)
      
class HtmxTest(View):
  def get(self,request):
      return render(request,"htmx_webpage.html")
      