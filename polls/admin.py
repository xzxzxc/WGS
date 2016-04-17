from django.contrib import admin
from polls.models import VisitorMessage


class VisitorMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'message', 'create')

admin.site.register(VisitorMessage, VisitorMessageAdmin)
