from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
import views
from django.views.static import serve
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^meetings/', include('meetings.urls', namespace="meetings")),
    url(r'^members/', include('members.urls', namespace="members")),
    url(r'^links/', include('links.urls', namespace="links")),
    url(r'^ua/', views.translate_ua, name='ua'),
    url(r'^en/', views.translate_en, name='en'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
	#url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, }),
    ]
