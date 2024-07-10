import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import asyncio
from datetime import datetime

from django.template.loader import get_template
from django.utils.html import format_html
from django.template import Context, Template

import random

class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("agent_tasks", self.channel_name) # Add to group to send messages later

    async def disconnect(self, close_code):
        pass
        # await self.channel_layer.group_discard("agent_tasks", self.channel_name)

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
        
        colors = [
        "#FF5733",  # Red-Orange
        "#33FF57",  # Lime Green
        "#3357FF",  # Blue
        "#F1C40F",  # Yellow
        "#9B59B6",  # Purple
        ]

        random_color = random.choice(colors)
        message = event['message']['message']
        template_string = """ 
        <div id="dynamic-content-ws" style='color: {{random_color}}'; hx-swap-oob="outerHTML"> 
            {{new_message|safe}}
        </div>
        """
        template = Template(template_string)
        context = Context({"new_message": message, "random_color":random_color})
    
        await self.send(text_data=template.render(context))