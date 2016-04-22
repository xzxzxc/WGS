from django.contrib import admin

from .models import Meeting, Report#, Author

admin.site.register(Meeting)
admin.site.register(Report)
#admin.site.register(Author)

# Register your models here.
