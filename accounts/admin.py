from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, MsnQual, AcftQual

class UserProfilesAdmin(admin.ModelAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
        'region',
        'user_supervisor',
        'is_supervisor',        
        )}),
    )

class CustomUserAdmin(UserAdmin):
    fieldsets = tuple(
        (fieldset[0], {
            **{key: value for (key, value) in fieldset[1].items() if key != 'fields'},
            'fields': fieldset[1]['fields'] + (
                'region',
                'user_supervisor',
                'is_supervisor',                 
            )
        })
        if fieldset[0] == 'Personal info'
        else fieldset
        for fieldset in UserAdmin.fieldsets
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MsnQual)
admin.site.register(AcftQual)
