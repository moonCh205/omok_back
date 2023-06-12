import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging 
logging.basicConfig(level='DEBUG')
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
    	# 파라미터 값으로 채팅 룸을 구별
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
    
        # 룸 그룹에 참가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sys_message',
                'messageType': 'system',
                'message': "%s(#%s)님 입장." % (self.scope['user']['nickname'],self.scope['user']['index']),
            }
        )
        await self.accept()

    async def disconnect(self, close_code):
        # 룸 그룹 나가기
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sys_message',
                'messageType': 'system',
                'message': "%s(#%s)님 퇴장." % (self.scope['user']['nickname'],self.scope['user']['index']),
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지 받음
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            sandTime = text_data_json['sandTime']
            message = text_data_json['message']
            # 룸 그룹으로 메세지 보냄
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'sandTime':sandTime,
                    'message': message,
                    'user' : self.scope['user']
                }
            )
        except:
            if 'event' in text_data_json:
                if text_data_json['event'] == 'rename':
                    self.scope['user']['nickname'] = text_data_json['value']

    # 룸 그룹으로부터 메세지 받음
    async def chat_message(self, event):
        user = event['user']
        sandTime = event['sandTime']
        message = event['message']
        # 웹소켓으로 메세지 보냄
        await self.send(text_data=json.dumps({
            'sandTime':sandTime,
            'message': message,
            'user': user,
        }))

    async def sys_message(self, event):
        messageType = event['messageType']
        message = event['message']
        # 웹소켓으로 메세지 보냄
        await self.send(text_data=json.dumps({
            'messageType': messageType,
            'message': message,
        }))