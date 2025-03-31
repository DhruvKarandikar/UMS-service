from django.db import models

class CommonUserReferrerModel(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    referrer = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name='referred_users')
    referee = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name='referrer')
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UserReferrer(CommonUserReferrerModel):
    
    class Meta:
        db_table = "ums_user_refer"
