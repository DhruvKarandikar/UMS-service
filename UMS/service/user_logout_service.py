from UMS.models import *
from custom_helpers.status_code import *
from custom_helpers.model_serializers_helpers import CustomExceptionHandler, validate_token, salt_and_hash
from UMS.serializers.user_logout_serializer import LogoutRequestSerializer


def logout_service(request):

    token_data = validate_token(request)

    request_data = request.data

    serialized_data = LogoutRequestSerializer(data=request_data)

    if not serialized_data.is_valid():
        return CustomExceptionHandler(ErrorClass.refresh_token_not_given)
    
    refresh_token_req = serialized_data.validated_data.get('refresh_token')

    try:
        old_ref_token = UserRefreshToken.objects.get(refresh_token=refresh_token_req)
    except:
        raise CustomExceptionHandler(ErrorClass.invalid_refresh_token)

    if old_ref_token:
        UserRefreshToken.objects.filter(refresh_token=old_ref_token.refresh_token).delete()
        return get_response(success)
    else:
        raise CustomExceptionHandler(generic_error_1)



def password_reset_service(request):

    from UMS.serializers.user_logout_serializer import RequestUserForgotPasswordSerializer

    request_data = request.data
    serializer = RequestUserForgotPasswordSerializer(data=request_data)

    if not serializer.is_valid():
        raise CustomExceptionHandler(generic_error_1)

    validated_data = serializer.validated_data

    email = validated_data.get('email_id', None)
    password = validated_data.get('password', None)

    user_obj = UserModel.objects.filter(email_id__iexact=email)
    if not user_obj.exists():
        raise CustomExceptionHandler(ErrorClass.user_not_found)

    get_user_uuid = user_obj.first().uuid_user
    new_secret_hash = salt_and_hash(get_user_uuid, password)

    new_user = user_obj.first()

    if not new_user:
        raise CustomExceptionHandler(ErrorClass.user_not_found)
    
    new_user.password_hash = new_secret_hash.upper()
    new_user.save()
    
    return get_response(success)

