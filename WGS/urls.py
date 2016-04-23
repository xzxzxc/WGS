from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from polls import views
from django.views.static import serve


urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^services/$', views.services, name='services'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^meetings/', include('meetings.urls', namespace="meetings")),
    url(r'^members/', include('members.urls', namespace="members")),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    ]

