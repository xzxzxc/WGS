from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from polls import views

urlpatterns = [
                  url(r'^$', views.home, name='home'),
                  url(r'^about/$', views.about, name='about'),
                  url(r'^services/$', views.services, name='services'),
                  url(r'^contacts/$', views.contacts, name='contacts'),
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^meetings/', include('meetings.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('', (
    r'^about/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), )
urlpatterns += patterns('', (
    r'^services/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), )
urlpatterns += patterns('', (
    r'^contacts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), )
