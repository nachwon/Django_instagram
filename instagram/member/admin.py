from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from member.models import User as CustomUser, Relationship


class RelationshipInline(admin.TabularInline):
    model = Relationship
    fk_name = 'from_user'
    extra = 1


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': (
                'nickname',
                'img_profile',
                'age',
                'user_type',
            )
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': (
                'nickname',
                'first_name',
                'last_name',
                'img_profile',
                'age',
            )
        }),
    )
    inlines = (RelationshipInline,)


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Relationship)
