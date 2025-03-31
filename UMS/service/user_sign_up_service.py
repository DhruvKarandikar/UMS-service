import uuid
from custom_helpers.status_code import *
from custom_helpers.model_serializers_helpers import CustomExceptionHandler, create_update_model_serializer, \
        salt_and_hash
import random
import string
from UMS.models import *
import logging
logger = logging.getLogger('django')


def referral_code_generator():
    referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return referral_code

def signup_user_service(request_data):

    from UMS.serializers.user_signup_serializer import HeadSignUpSerializer, DataSerializer, UserReferrerSerializer

    password = request_data.get('password')
    referral_code = request_data.get('referral_code')

    if request_data.get('email_id'):
        obj = UserModel.objects.filter(email_id__iexact=request_data.get('email_id'))

        if len(obj) > 0:
            raise CustomExceptionHandler(ErrorClass.email_exists) 

    user_uuid = uuid.uuid4()

    secret_hash = salt_and_hash(str(user_uuid), password)
    request_data['password_hash'] = secret_hash.upper()
    request_data['uuid_user'] = str(user_uuid)
    request_data['user_referral_code'] = referral_code_generator()
    
    if referral_code:
        user_obj = UserModel.objects.filter(user_referral_code=referral_code).first()
        request_data['referred_by_id'] = user_obj.id

    final_data = {}

    signup_data_instance = create_update_model_serializer(HeadSignUpSerializer,request_data,partial=True)
    serializer_obj = None

    if signup_data_instance.referred_by and signup_data_instance.id:       
        new_referer_data = {
            "referrer_id": signup_data_instance.id,
            "referee_id": signup_data_instance.referred_by_id,
        }
        user_referrer_instance = create_update_model_serializer(UserReferrerSerializer, new_referer_data, partial=True)

    if signup_data_instance:
        serializer_obj = DataSerializer(signup_data_instance)

    final_data = serializer_obj.data

    if not serializer_obj:
        return CustomExceptionHandler(generic_error_1)

    return get_response(success, data=final_data)

