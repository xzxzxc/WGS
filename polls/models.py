from django.db import models


class VisitorMessage(models.Model):
    email = models.EmailField(max_length=30)
    message = models.TextField(max_length=30)
    create = models.DateTimeField(auto_now=True)
