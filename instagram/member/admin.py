from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from member.models import User as CustomUser


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('img_profile', 'age', 'user',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {'fields': ('img_profile', 'age',)}),
    )
    pass


admin.site.register(CustomUser, UserAdmin)
