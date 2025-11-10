from django.contrib import admin
from .models import UserToken,Otp
# Register your models here.
admin.site.register(UserToken)
admin.site.register(Otp)