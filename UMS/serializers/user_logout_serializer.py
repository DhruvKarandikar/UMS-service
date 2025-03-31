from rest_framework import serializers
from UMS.models import *
from custom_helpers.model_serializers_helpers import CustomExceptionHandler
from custom_helpers.consts import *
import re
from custom_helpers.status_code import *
from UMS.serializers.user_signup_serializer import password_regex


class LogoutRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    
    class Meta:
        model = UserRefreshToken
        fields = ("refresh_token",)

    def validate_refresh_token(self, value):
        if value in ["", None]:
            raise CustomExceptionHandler(ErrorClass.refresh_token_not_given)
    
        return value


class LogoutResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)

    class Meta:
        model = UserModel
        fields = ("status", "message",)


class RequestUserForgotPasswordSerializer(serializers.ModelSerializer):

    email_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = UserModel
        fields = ("email_id", "password",)
    
    def validate(self, data):
        data = super().validate(data)
        return {key: value for key, value in data.items() if value is not None}

    def validate_email_id(self,value):
        
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  
        if not re.fullmatch(regex, value):
            raise CustomExceptionHandler(ErrorClass.email_id_incorrect)

        return value        

    # def validate_password(self, value):

    #     if value:
    #         bool_regex = password_regex(value)

    #         if bool_regex == False:
    #             raise CustomExceptionHandler(ErrorClass.password_regex_error)

    #     return value


class ResponseUserForgotPasswordSerializer(serializers.Serializer):

    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)

    class Meta:
        model = UserModel
        fields = ("status", "message",)
