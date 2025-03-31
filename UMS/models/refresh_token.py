from django.db import models
from UMS.models.user_model import UserModel

class CommonUserRefreshToken(models.Model):
    refresh_token = models.TextField(primary_key=True)
    user = models.ForeignKey(to=UserModel, related_name='refresh_user', on_delete=models.RESTRICT, null=False)

    class Meta:
        abstract = True


class UserRefreshToken(CommonUserRefreshToken):

    class Meta:
        db_table = "ums_user_refresh_token"


