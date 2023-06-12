import redis
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserInfo
from .serializers import UserInfoSerializer
from .middlewares import returnUser,updateUser,returnRoom,makeRoom
from django.http import JsonResponse 
import json
import logging 
logging.basicConfig(level='DEBUG')

@api_view(['GET','PUT'])
def userAPI(request, id):

    if request.method == 'GET':
        # user =json.dumps( returnUser(id), ensure_ascii=False).encode('utf-8')
        user = returnUser(id)
    elif request.method == 'PUT':
        try:
            query_str = {
                "key" : request.GET['key'],
                "value" : request.GET['value']
            }
          
            user = updateUser(id,query_str)
            logging.info('updateUser 끝')
        except:
            return Response("invalid request", status=400)
    
    return JsonResponse(user,status=200)

@api_view(['GET','POST'])
def roomAPI(request, id):

    if request.method == 'GET':
        # user =json.dumps( returnUser(id), ensure_ascii=False).encode('utf-8')
        room_data = returnRoom(id,20)
    elif request.method == 'POST':
        try:
            room_name = request.GET['room_name']
            room_data = makeRoom(room_name)
        except:
            return Response("invalid request", status=400)
    
    return JsonResponse(room_data,status=200)

