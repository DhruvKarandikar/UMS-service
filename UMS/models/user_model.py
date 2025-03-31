from django.db import models

class CommonUserModel(models.Model):

    id = models.BigAutoField(primary_key=True)
    uuid_user = models.TextField(null=False, unique=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email_id = models.TextField(null=False, unique=True)
    mobile_no = models.CharField(null=False, unique=True)
    password_hash = models.TextField(null=False)
    gender = models.IntegerField(null=False)
    user_referral_code  = models.TextField(null=True, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals') 

    class Meta:
        abstract = True


class UserModel(CommonUserModel):
    
    class Meta:
        db_table = "ums_user"
