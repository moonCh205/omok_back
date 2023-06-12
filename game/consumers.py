import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging 
# logger.debug()
# logger.info()
# logger.warning()
# logger.error()
# logger.critical()

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
    	# 파라미터 값으로 채팅 룸을 구별
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        users = self.scope['user']
        # 룸 그룹에 참가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 룸 그룹 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지 받음
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        player = text_data_json['player']
        x = text_data_json['x']
        y = text_data_json['y']
        # 룸 그룹으로 메세지 보냄
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', #함수이름
                'player': player,
                'x': x,
                'y':y,
                # 'pk':username,
            }
        )

    # 룸 그룹으로부터 메세지 받음
    async def chat_message(self, event):
        player = event['player']
        x = event['x']
        y = event['y']
     
        # pk = event['pk']
        # 웹소켓으로 메세지 보냄
        await self.send(text_data=json.dumps({
            'player': player,
            'x': x,
            'y':y,
            # 'pk':pk
        }))