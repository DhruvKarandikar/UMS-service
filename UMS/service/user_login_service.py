from custom_helpers.status_code import *
from custom_helpers.model_serializers_helpers import CustomExceptionHandler, salt_and_hash, generate_token_pair, validate_token
from custom_helpers.model_serializers_helpers import create_update_model_serializer
from UMS.models import *
import logging

logger = logging.getLogger('django')

def password_verification(user_object, secret):

    user_uuid = user_object.first().uuid_user
    password = user_object.first().password_hash
    user_id = user_object.first().id

    refresh_token_obj = UserRefreshToken.objects.filter(user_id=user_id).first()

    if password == salt_and_hash(user_uuid, secret).upper():
        access_token, refresh_token = generate_token_pair(user_object)

        if refresh_token_obj:
            refresh_token = refresh_token_obj.refresh_token
        else:
            UserRefreshToken.objects.create(refresh_token=refresh_token, user_id=user_id)
    else:
        raise CustomExceptionHandler(ErrorClass.invalid_valid_credentials)

    return access_token, refresh_token


def login_user_service(request_data):
    from UMS.serializers.user_login_serializer import UserLoginRequestSerializer

    serialized_data = UserLoginRequestSerializer(data=request_data)

    if not serialized_data.is_valid():
        raise CustomExceptionHandler(generic_error_3)

    email_id = serialized_data.data.get('email_id')
    password =  serialized_data.data.get('password')

    user_obj = UserModel.objects.filter(email_id__iexact=email_id)

    if not user_obj:
        raise CustomExceptionHandler(ErrorClass.user_not_found)

    if len(user_obj) > 1:
        raise CustomExceptionHandler(ErrorClass.email_exists)

    access_token, refresh_token = password_verification(user_obj, password)

    return get_response(success, data={"access_token": access_token, "refresh_token": refresh_token})


def get_user_service(request):

    from UMS.serializers.user_signup_serializer import DataSerializer

    token_data = validate_token(request)
    uuid_user = token_data.get('user_uuid')
    user_id = token_data.get('user_id')

    validate_data = request.validation_serializer.validated_data

    user_obj = UserModel.objects.filter(uuid_user__iexact=uuid_user, id=user_id).first()

    if not user_obj:
        raise CustomExceptionHandler(ErrorClass.user_not_found)

    obj_data = []

    serialized_obj = DataSerializer(user_obj)

    if serialized_obj:
        obj_data = serialized_obj.data

    return get_response(success, data=obj_data)

