from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from polls.forms import VisitorMessageForm
from polls.models import VisitorMessage


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# def my(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


def home(request):
    if request.method == "POST":
        form = VisitorMessageForm(request.POST)
        message = form.cleaned_data['message']
        obj = VisitorMessage(message=message)
        obj.save()
    return render(request, "home.html")
