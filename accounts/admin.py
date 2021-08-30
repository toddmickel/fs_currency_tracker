from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MsnQual, AcftQual

admin.site.register(User, UserAdmin)
admin.site.register(MsnQual)
admin.site.register(AcftQual)
