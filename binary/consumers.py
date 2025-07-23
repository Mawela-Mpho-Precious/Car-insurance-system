import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.car_id = self.scope['url_route']['kwargs']['car_id']
        self.car_group_name = f'car_{self.car_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.car_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.car_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        location = data['location']
        status = data['status']
        speed = data['speed']

        # Send message to room group
        await self.channel_layer.group_send(
            self.car_group_name,
            {
                'type': 'car_update',
                'location': location,
                'status': status,
                'speed': speed,
            }
        )

    # Receive message from room group
    async def car_update(self, event):
        location = event['location']
        status = event['status']
        speed = event['speed']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'location': location,
            'status': status,
            'speed': speed,
        }))