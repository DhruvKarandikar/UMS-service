from django.db.models.query import Q
from rest_framework.serializers import ModelSerializer
import hashlib
from custom_helpers.consts import *
from custom_helpers.status_code import *
import logging
import jwt

logger = logging.getLogger('django')

def dict_get_key_from_value(dict_obj, dict_val):
    try:
        if dict_val is not None:
            key_list = list(dict_obj.keys())
            val_list = list(dict_obj.values())
            try:
                position = val_list.index(int(dict_val))
            except:
                position = val_list.index(dict_val)
            return key_list[position]
        else: 
            return None 
    except:
        return None

def help_text_for_dict(dict_value):
    """
    Args:
        dict_value (_type_): Dict type

    Returns:
        _type_: String Format help text
    """
    return f'Enter value from this list - {list(dict_value.keys())}'


def common_checking_and_passing_value_from_list_dict(value, list_dict, error_label):
    """
    merged two functions common_dict_checking_and_passing_value, common_list_checking
    """
    if value == "":
        return None

    if value:
        if type(list_dict) == list:
            if value not in list_dict:
                raise CustomExceptionHandler(error_label)
            return value
        else:
            if type(value) == list:
                list_value = []
                for single_value in value:
                    if single_value not in list_dict.keys():
                        raise CustomExceptionHandler(error_label)
                    list_value.append(list_dict[single_value])
                return list_value
            
            if value not in list_dict.keys():
                raise CustomExceptionHandler(error_label)
                    
            return list_dict[value]
    return value

def get_model_data(modelName, q_parameter, error_code_1, error_code_2, no_obj_flag=False, multiple_obj_flag=False):
    try:
        return modelName.objects.get(q_parameter)
    except modelName.MultipleObjectsReturned as e:
        if multiple_obj_flag is True:
            return modelName.objects.filter(q_parameter)
        raise CustomExceptionHandler(error_code_1)
    except modelName.DoesNotExist as e:
        if no_obj_flag is True:
            return None
        raise CustomExceptionHandler(error_code_2)

def create_update_model_serializer(model_serializer: ModelSerializer, data: dict, additional_data: dict = {}, partial=False):

    """
    Mainly it performs  create and update   functions 
    This function takes a model serializer, data, additional data, and a partial flag as input parameters.
    It validates the data using the provided model serializer and returns the instance if the data is valid.
    Returns:
    - instance: The instance of the model if the data is valid.

    Raises:
    - CustomExceptionHandler: If there is an error in the serializer.

"""
    id = data.get('id')
    model = model_serializer.Meta.model
    if id:
        instance = get_model_data(model, Q(id=id), None, obj_not_found(id,model.__name__)) 
        serializer = model_serializer(instance, data=data, partial=True, context=additional_data)
    else:
        serializer = model_serializer(data=data, partial=partial, context=additional_data)

    if not serializer.is_valid():
        logger.error(f"error in serilizer is {serializer.errors}")
        raise CustomExceptionHandler(error_in_serializer(model_serializer))
    serializer.validated_data.update(additional_data)
    instance=serializer.save()
    return instance


def comman_create_update_services(self, validated_data, instance = None):

    if not instance:
        instance = self.Meta.model.objects.create(**validated_data)

    else:
        updated_keys = []
        for key, value in validated_data.items():
            if value != None and key != 'id':
                updated_keys.append(key)
                setattr(instance, key, value)
        instance.save(update_fields = updated_keys)

    return instance


class CustomExceptionHandler(Exception):
    def __init__(self, message=''):
        # Call the base class constructor with the parameters it needs
        super(CustomExceptionHandler, self).__init__(message)


def salt_and_hash(prefix, credential):
    return hashlib.sha256((prefix + credential + SALTING_CONSTANT).encode()).hexdigest()

def generate_token_pair(user_object, get_access_token=True, get_refresh_token=True, access_token_extra_data = {}):
    
    user_obj = user_object.first()

    access_token_payload = {"user_id": user_obj.id,"user_uuid": user_obj.uuid_user, "sub": "access_token"}
    refresh_token_payload = {"user_id": user_obj.id, "user_uuid": user_obj.uuid_user, "sub": "refresh_token"}
    
    access_token, refresh_token= None, None
    access_token_payload.update(access_token_extra_data)

    if get_access_token:
        access_token = jwt.encode(payload=access_token_payload, key = JWT_KEY_PRIVATE, algorithm=ALGORITHM_OF_JWT)

    if get_refresh_token:
        refresh_token = jwt.encode(
            payload=refresh_token_payload, key = JWT_KEY_PRIVATE, algorithm=ALGORITHM_OF_JWT)
        
    return access_token, refresh_token


def validate_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    
    if not auth_header:
        raise CustomExceptionHandler(generic_error_4)

    token = auth_header.split(" ")[1]

    try:
        token_data = jwt.decode(token, public_key, algorithms=[ALGORITHM_OF_JWT])
        
        uuid_user = token_data.get('user_uuid')
        user_id = token_data.get('user_id')

        logger.debug(f"Decoded Token Data: {token_data}")

    except jwt.ExpiredSignatureError:
        raise CustomExceptionHandler("Token has expired.")
    except jwt.InvalidTokenError:
        raise CustomExceptionHandler("Invalid token.")
    

    return {
        'request': request,
        'user_uuid': uuid_user,
        'user_id': user_id,
    }
