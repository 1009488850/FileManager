from django.contrib import admin
from sharefile import models
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('login_user','pub_date','last_modify')

admin.site.register(models.UserProfile,UserProfileAdmin)