from django.db import models


class Meeting(models.Model):
    topic_text = models.CharField(max_length=50)
    detail_text = models.TextField()
    meeting_date = models.DateField('time of meeting')
    pub_date = models.DateField('date published')

    def __unicode__(self):  # __unicode__ on Python 2
        return self.meeting_topic_text
