# chatapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message
import json
class ChatConsumer(AsyncWebsocketConsumer):
    # A consumer for WebSocket connections
    async def connect(self):
        # Accept the connection
        await self.accept()
        # Join the chat group
        await self.channel_layer.group_add('chat', self.channel_name)

    async def disconnect(self, close_code):
        # Leave the chat group
        await self.channel_layer.group_discard('chat', self.channel_name)

    async def receive(self, text_data):
        # Receive a message from the WebSocket
        data = json.loads(text_data)
        # Save the message to the database
        message = Message.objects.create(
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            content=data['content']
        )
        # Send the message to the chat group
        await self.channel_layer.group_send(
            'chat',
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Receive a message from the chat group
        message = event['message']
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'content': message.content,
            'timestamp': message.timestamp
        }))
