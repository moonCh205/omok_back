
from urllib.parse import parse_qs
import json
import redis

import logging 
logging.basicConfig(level='DEBUG')

# 채팅관련
def updateUser(id,data):
    rd = redis.StrictRedis(host='localhost', port=6379, db=0)
    if data['key'] != 'index':
        try:
            user = rd.get(id)
            user = user.decode('utf-8')
            user = dict(json.loads(user))
            if data['key'] in user:
                user[data['key']] = data['value']
                jsonDataDict = json.dumps(user, ensure_ascii=False).encode('utf-8')
                rd.set(id, jsonDataDict)
                jsonRespone = user
            else:
                jsonRespone = {
                    "error": "400",
                }
        except:
            jsonRespone = {
                "error": "Not a login ID",
            }
    else:
        jsonRespone = {
                "error": "400",
        }
    # jsonRespone = json.dumps(jsonRespone, ensure_ascii=False).encode('utf-8')
    return jsonRespone

def returnUser(key_string):
    rd = redis.StrictRedis(host='localhost', port=6379, db=0)
    if len(key_string) > 20:
        try:
            user = rd.get(key_string)
            user = user.decode('utf-8')
            dataDict = dict(json.loads(user))
        except:
            try:
                user_index = rd.get('index')
                user_index = int(user_index)
            except:
                user_index = 1
            dataDict = {
                "index":user_index,
                "nickname": "noname",
                "win": "0",
                "defeat": "0"
            }
            jsonDataDict = json.dumps(dataDict, ensure_ascii=False).encode('utf-8')
            user_index += 1
            
            rd.set(key_string, jsonDataDict)
            rd.set('index', user_index)      
    else:
        dataDict = {
                "error": "400",
        }
        
    return dataDict
 
def isUser(key_string):
    rd = redis.StrictRedis(host='localhost', port=6379, db=0)
    respone = False
    try:
        user = rd.get(key_string)
        user = user.decode('utf-8')
        user = dict(json.loads(user))
        respone = True
    except:
        respone = False
    return respone

    # 방만들기 관련 (방 인원수는  zrange asgi:group:chat_game${room_index} 0 -1) 
def makeRoom(room_name):
    rd = redis.StrictRedis(host='localhost', port=6379, db=0)
    try:
        room_index = rd.get('room_index')
        room_index = int(room_index)
    except:
        room_index = 1
    dataDict = {
        "room_name": room_name,
        "start": False,
    }
    jsonDataDict = json.dumps(dataDict, ensure_ascii=False).encode('utf-8')
    try:
        rd.zadd('room', {jsonDataDict:room_index})
        room_index += 1
        rd.set('room_index', room_index)
        respone = {
            "state": "200",
        }    
    except:
        respone = {
            "error": "400",
        }
    return respone

def returnRoom(index,need_count):
    # need_count -1 == 전체 조회
    # {room_name:valus , room_index:valus , count : valus, start:valus}
    rd = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    try:
        # rd.zrange('room', index, need_count, withscores=True) [(b'a', 0.0), (b'b', 5.0), (b'c', 8.0), (b'd', 20.0)]
        room_list = rd.zrange('room', index, need_count,withscores=True)
        logging.info(room_list)
        jsonRespone = []
        for room_data in room_list :
            dict_data = room_data[0].decode('utf-8')
            dict_data = dict(json.loads(dict_data))
            key = 'asgi:group:game_%d' % room_data[1]
            personnel = rd.zrange(key, 0, -1)
            personnel = len(personnel)
            
            data = {
                'count': personnel,
                'index' : room_data[1],
                'start' : dict_data['start'],
                'room_name' : dict_data['room_name'],
            }
            jsonRespone.append(data)
    except:
        jsonRespone = {
            "error": "400",
        }
            
    # jsonRespone = json.dumps(jsonRespone, ensure_ascii=False).encode('utf-8')
    return jsonRespone

class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app
 
    async def __call__(self, scope, receive, send,):
        path_string = scope["path"]
        
        path_string = path_string.lstrip("/")
        path_string = path_string.split('/').pop()
        user = returnUser(path_string)
        scope["user"] = user
        return await self.app(scope, receive, send)
