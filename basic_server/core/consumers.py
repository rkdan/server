import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from datetime import datetime

class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("agent_tasks", self.channel_name) # Add to group to send messages later

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("agent_tasks", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('type') == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))
        else:
            message = text_data_json['message']
            await self.channel_layer.group_send(
                "chat",
                {
                    'type': 'agent_message',
                    'message': json.dumps(message)
                }
            )
    
    async def agent_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))