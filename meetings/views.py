from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .models import Meeting


class IndexView(generic.ListView):
    template_name = 'meetings/index.html'
    context_object_name = 'latest_meeting_list'

    def get_queryset(self):
        """
        Return the last ten published meetings (not including those set to be
        published in the future).
        """
        return Meeting.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Meeting
    template_name = 'meetings/detail.html'

    def get_queryset(self):
        return Meeting.objects.all()

