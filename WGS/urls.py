from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from polls import views
from django.views.static import serve
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
     {'next_page': '/'}),
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^services/$', views.services, name='services'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^meetings/', include('meetings.urls', namespace="meetings")),
    url(r'^members/', include('members.urls', namespace="members")),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    ]

