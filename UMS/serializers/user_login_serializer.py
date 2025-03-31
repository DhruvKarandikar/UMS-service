from rest_framework import serializers
from django.db.models import Q
from UMS.models import *
from django.db.transaction import atomic
from custom_helpers.model_serializers_helpers import CustomExceptionHandler, comman_create_update_services
from custom_helpers.consts import *
import re
from custom_helpers.status_code import *
from UMS.serializers.user_signup_serializer import DataSerializer

class UserLoginRequestSerializer(serializers.Serializer):
    email_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = UserModel
        fields = ("email_id", "password",)
    
    def validate_email_id(self,value):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  
        if not re.fullmatch(regex, value):
            raise CustomExceptionHandler(ErrorClass.email_id_incorrect)  
        return value
    
    

class SigninDataResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)
    
    class Meta:
        model = UserRefreshToken
        fields = ("access_token", "refresh_token",)


class UserLoginResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = SigninDataResponseSerializer(required=False) 

    class Meta:
        model = UserModel
        fields = ("status", "message","data",)



class GetUserRequestSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=True)

    class Meta:
        model = UserModel
        fields = ("id",)


class GetUserResponseSerializer(serializers.ModelSerializer):

    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = DataSerializer(required=False)

    class Meta:
        model = UserModel
        fields = ("status", "message", "data",)
