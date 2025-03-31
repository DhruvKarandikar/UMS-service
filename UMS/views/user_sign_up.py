import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from custom_helpers.status_code import get_response, generic_error_2
from custom_helpers.model_serializers_helpers import CustomExceptionHandler
from UMS.serializers.user_signup_serializer import UserSignUpRequestSerializer, UserSignUpResponseSerializer
from UMS.service.user_sign_up_service import signup_user_service

logger = logging.getLogger("django")


@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body=UserSignUpRequestSerializer,
    responses={"200": UserSignUpResponseSerializer},
    operation_id="User Sign Up"
)
@api_view(["POST"])
def user_signup_api(request):
    response_obj = None

    try:
        logger.debug(f"{request.data}, request for user signup")
        response_obj = signup_user_service(request.data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in user signup url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in user signup url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in user signup --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)

