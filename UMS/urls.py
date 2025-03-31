from django.urls import path
from .views import *

urlpatterns = [
    path('user_login', user_login_api, name='user_sign_in'),
    path('user_signup', user_signup_api, name='user_sign_up'),
    path('user_logout', user_logout_api, name='user_logout'),
    path('get_user', get_user_api, name='get_user_details'),
    path('reset_password', password_forgot_view, name='reset_password_url'),
]