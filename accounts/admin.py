from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, MsnQual, AcftQual

admin.site.register(CustomUser, UserAdmin)
admin.site.register(MsnQual)
admin.site.register(AcftQual)
