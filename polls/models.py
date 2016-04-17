import datetime
from django.db import models
from django.utils import timezone


<<<<<<< HEAD
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
=======
class VisitorMessage(models.Model):
    email = models.EmailField(max_length=30)
    message = models.TextField(max_length=30)
    create = models.DateTimeField(auto_now=True)
>>>>>>> origin/Vlad
