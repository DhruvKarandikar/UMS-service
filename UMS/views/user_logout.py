import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from custom_helpers.status_code import get_response, generic_error_2
from custom_helpers.model_serializers_helpers import CustomExceptionHandler
from UMS.serializers.user_logout_serializer import LogoutRequestSerializer, LogoutResponseSerializer, \
    RequestUserForgotPasswordSerializer, ResponseUserForgotPasswordSerializer
from UMS.service.user_logout_service import logout_service, password_reset_service

logger = logging.getLogger("django")


@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body=LogoutRequestSerializer,
    responses={"200": LogoutResponseSerializer},
    operation_id="User Logout"
)
@api_view(["POST"])
def user_logout_api(request):
    response_obj = None

    try:
        logger.debug(f"{request.data}, request for user logout")
        response_obj = logout_service(request)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in user logout url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in user logout url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in user logout --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)



@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body=RequestUserForgotPasswordSerializer,
    responses={"200": ResponseUserForgotPasswordSerializer},
    operation_id="User Password Reset"
)
@api_view(["POST"])
def password_forgot_view(request):
    response_obj = None

    try:
        logger.debug(f"{request.data}, request for password reset")
        response_obj = password_reset_service(request)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in password reset url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in password reset url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in password reset --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)

