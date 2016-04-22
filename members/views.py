from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from .models import Member


class IndexView(generic.ListView):
    template_name = 'members/index.html'
    context_object_name = 'latest_member_list'

    def get_queryset(self):
        # Return latest joined members
        return Member.objects.filter(join_date__lte=timezone.now()).order_by('-join_date')[:10].reverse()


class DetailView(generic.DetailView):
    model = Member
    template_name = 'members/detail.html'
