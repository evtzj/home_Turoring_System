import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.room_group_name = f"chat_{self.match_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get("content", "")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "content": content,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "match_id": self.match_id,
            "content": event["content"],
        }))
