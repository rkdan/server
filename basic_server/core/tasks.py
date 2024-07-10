from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def add(args):
  
  out = args['x'] + args['y']

  message = {
  "status": "TASK HAS RAN SUCCESSFULLY", 
  "message": out,
  }

  # Use Channels layer to send the message via Web Socket
  channel_layer = get_channel_layer()
  async_to_sync(channel_layer.group_send)(
      'agent_tasks', # Sends the message to the AGENT_TASKS group
      {
          "type": 'agent_message',  # This corresponds to the Consumer method to call
          "message": message
      }
  )