from django.shortcuts import render
from django.http import HttpResponse
from WGS.settings import DOMAIN_NAME
from polls.forms import VisitorMessageForm
from polls.models import VisitorMessage


def home(request):
    if request.method == "POST":
        form = VisitorMessageForm(request.POST)
        message = form.cleaned_data['message']
        obj = VisitorMessage(message=message)
        obj.save()

    first_message = VisitorMessage.objects.filter()[0]
    return render(request, "home.html", {"DOMAIN_NAME": DOMAIN_NAME, "first_message": first_message})


def about(request):
    return render(request, "about.html", {"DOMAIN_NAME": DOMAIN_NAME})


def services(request):
    return render(request, "services.html", {"DOMAIN_NAME": DOMAIN_NAME})


def contacts(request):
    return render(request, "contacts.html", {"DOMAIN_NAME": DOMAIN_NAME})

