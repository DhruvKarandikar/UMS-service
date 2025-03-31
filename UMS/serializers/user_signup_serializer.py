from rest_framework import serializers
from django.db.models import Q
from UMS.models import *
from django.db.transaction import atomic
from custom_helpers.model_serializers_helpers import dict_get_key_from_value, help_text_for_dict \
    , CustomExceptionHandler, comman_create_update_services, common_checking_and_passing_value_from_list_dict
from custom_helpers.consts import *
import re
from custom_helpers.status_code import *


def password_regex(password):

    if len(password) < 8:
        return False

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'

    return re.match(pattern, password) is not None


class HeadSignUpSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    email_id = serializers.CharField(required=True)
    mobile_no = serializers.CharField(required=True)
    password_hash = serializers.CharField(required=True)
    gender = serializers.CharField(required=True, help_text=help_text_for_dict(gender_dict))
    user_referral_code = serializers.CharField(required=False)
    referred_by_id = serializers.IntegerField(required=False)

    class Meta:
        model = UserModel
        fields = '__all__'
        depth = 2
    
    def validate_gender(self,value):
        return common_checking_and_passing_value_from_list_dict(value, gender_dict, ErrorClass.gender_incorrect)


    def validate_uuid_user(self, value):
        if value in [None, "", 0]:
            raise CustomExceptionHandler(ErrorClass.uuid_user_none)

        if UserModel.objects.filter(uuid_user__iexact=value).exists():
            raise CustomExceptionHandler(ErrorClass.uuid_user_exists)

        return value

    def validate(self, data):
        data = super().validate(data)
        return {key: value for key, value in data.items() if value is not None}

    @atomic
    def create(self, validated_data):
        return comman_create_update_services(self, validated_data)

    @atomic
    def update(self, instance, validated_data):
        return comman_create_update_services(self, validated_data, instance)


    def to_representation(self, data):
        data = super().to_representation(data)

        if data.get('gender'):
            data['gender'] = dict_get_key_from_value(gender_dict, data['gender'])

        return data


class UserSignUpRequestSerializer(HeadSignUpSerializer):
    password_hash = None
    referred_by = None
    password = serializers.CharField(required=True)
    referral_code = serializers.CharField(required=False)

    class Meta:
        model = UserModel
        fields = ("id", "first_name","last_name","email_id","mobile_no","gender", "password", "referral_code",)
 
    def validate_email_id(self,value):
        
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  
        if not re.fullmatch(regex, value):
            raise CustomExceptionHandler(ErrorClass.email_id_incorrect)

        return value

    def validate_password(self,value):

        if value:
            bool_regex = password_regex(value)

            if bool_regex == False:
                raise CustomExceptionHandler(ErrorClass.password_regex_error)

        return value



class UserSignUpResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = UserSignUpRequestSerializer(required=False)

    class Meta:
        model = UserModel
        fields = ("status", "message", "data",)


class UserReferrerSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    referrer_id = serializers.IntegerField(required=True)
    referee_id = serializers.IntegerField(required=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        model = UserReferrer
        fields = ("id", "referrer_id", "referee_id", "registration_date",)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        referrer = UserModel.objects.filter(id=instance.referrer_id).first()
        referee = UserModel.objects.filter(id=instance.referee_id).first()
        
        data["registration_date"] = instance.registration_date.date()
        data["referrer_name"] = f"{referrer.first_name} {referrer.last_name}" if referrer else None
        data["referrer_email"] = f"{referrer.email_id}"
        data["referee_name"] = f"{referee.first_name} {referee.last_name}" if referee else None
        data["referee_email"] = f"{referee.email_id}"

        return data


class DataSerializer(HeadSignUpSerializer):

    referred_by = None
    user_referrer = UserReferrerSerializer(many=True, source='referred_users')

    class Meta:
        model = UserModel
        fields = ("id", "first_name","last_name","email_id","mobile_no","gender","user_referrer",)

