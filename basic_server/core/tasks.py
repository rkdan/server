from celery import shared_task

@shared_task
def add(args):
  
  out = args['x'] + args['y']

  message = {
  "status": "TASK HAS RAN SUCCESSFULLY", 
  "message": out,
  }

  print(message)