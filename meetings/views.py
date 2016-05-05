from django.views import generic
from django.utils import timezone
from .models import Meeting
import datetime
from django.http import Http404


class IndexView(generic.ListView):
    template_name = 'meetings/index.html'
    context_object_name = 'latest_meeting_list'

    def get_queryset(self):
        return Meeting.objects.filter(meeting_date__lte=timezone.now() + datetime.timedelta(weeks=1)).order_by(
            '-meeting_date')[:10]


class DetailView(generic.DetailView):
    model = Meeting
    template_name = 'meetings/detail.html'

    def get_object(self):
        object = super(DetailView, self).get_object()
        if object.meeting_date > datetime.date.today() + datetime.timedelta(weeks=1):
            raise Http404
        return object
