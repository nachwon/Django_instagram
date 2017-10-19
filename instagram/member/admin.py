from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from member.models import User as CustomUser


admin.site.register(CustomUser, UserAdmin)
