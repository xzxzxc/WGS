from django.utils import translation
from django.http import HttpResponseRedirect
from django.shortcuts import render


def about(request):
    return render(request, "about.html")


def home(request):
    return render(request, "home.html")


def translate_ua(request):
    user_language = 'uk'
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def translate_en(request):
    user_language = 'en'
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
