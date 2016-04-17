from django.contrib import admin
<<<<<<< HEAD
from .models import Question

admin.site.register(Question)

=======
from polls.models import VisitorMessage


class VisitorMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'message', 'create')

admin.site.register(VisitorMessage, VisitorMessageAdmin)
>>>>>>> origin/Vlad
