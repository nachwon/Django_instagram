from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from member.models import User as CustomUser, Relationship


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': (
                'nickname',
                'img_profile',
                'age',
                'user_type'
            )
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': (
                'nickname',
                'img_profile',
                'age',
            )
        }),
    )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Relationship)
