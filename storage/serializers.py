from rest_framework import serializers
from .models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    class meta:
        model = UserInfo
        fields = ('nickname','win','defeat')