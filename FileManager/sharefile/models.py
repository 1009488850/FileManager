from django.db import models
from django.contrib.auth.models import User
from sharefile.perm_conf import perms
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    login_user = models.CharField(max_length=255,verbose_name=u"登录用户")
    pub_date = models.DateTimeField(verbose_name=u"创建时间")
    last_modify = models.DateTimeField(auto_now=True,verbose_name=u"修改时间")

    def __str__(self):
        return self.login_user
    class Meta:
        permissions = perms


class UpDownFile(models.Model):

    upload_file = models.CharField(max_length=255,unique=True)
    upload_user = models.ForeignKey('UserProfile')
    upload_date = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.upload_user
