import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from custom_helpers.status_code import get_response, generic_error_2
from custom_helpers.model_serializers_helpers import CustomExceptionHandler
from UMS.serializers.user_login_serializer import UserLoginRequestSerializer, UserLoginResponseSerializer, \
    GetUserRequestSerializer, GetUserResponseSerializer
from custom_helpers.custom_decorator import custom_api_view
from UMS.service.user_login_service import login_user_service, get_user_service

logger = logging.getLogger("django")


@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body=UserLoginRequestSerializer,
    responses={"200": UserLoginResponseSerializer},
    operation_id="User Login"
)
@api_view(["POST"])
def user_login_api(request):
    response_obj = None

    try:
        logger.debug(f"{request.data}, request for user signup")
        response_obj = login_user_service(request.data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in user signup url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in user signup url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in user signup --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)


@csrf_exempt
@custom_api_view(
    request_serializer=GetUserRequestSerializer,
    responses={"200": GetUserResponseSerializer},
    operation_id="Get User"
)
def get_user_api(request):
    response_obj = None

    try:
        logger.info("request for get user: %s", request.validation_serializer.validated_data)
        response_obj = get_user_service(request)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in get user: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in get user {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in get user --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)


