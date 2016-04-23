from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Student, Professor


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class MemberInline(admin.TabularInline):
#     model = Member
#     can_delete = False
#     verbose_name_plural = 'member'
#
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (MemberInline, )
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

admin.site.register(Student)
admin.site.register(Professor)


