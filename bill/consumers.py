# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer

class BillConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.bill_group_name = "bill_status_updates"

        # Retrieve and add the channel layer
        self.channel_layer = get_channel_layer()
        await self.channel_layer.group_add(self.bill_group_name, self.channel_name)

    async def disconnect(self, close_code):
        # Remove the client from the group when disconnected
        await self.channel_layer.group_discard(self.bill_group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_message(self, event):
        # Send a message to the WebSocket
        await self.send(text_data=json.dumps(event))

    async def bill_update(self, event):
        # Handle bill update signals
        await self.send_message({"message": event["message"]})
