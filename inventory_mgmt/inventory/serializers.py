from rest_framework import serializers
from django.contrib.auth import  authenticate
from .models import *
from django.contrib.auth.password_validation import validate_password

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 255,write_only = True)
    password = serializers.CharField(max_length = 255,write_only = True)

    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
