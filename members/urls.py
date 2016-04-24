from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^professor/(?P<pk>[0-9]+)/$', views.DetailProfessorView.as_view(), name='professor_detail'),
    url(r'^student/(?P<pk>[0-9]+)/$', views.DetailStudentView.as_view(), name='student_detail'),
    url(r'^profile/$', views.profile_view, name='profile_view'),
    url(r'^profile/professor/$', views.ProfileProfessorView.as_view(), name='profile_professor_view'),
    url(r'^profile/student/$', views.ProfileStudentView.as_view(), name='profile_student_view'),
    url(r'^profile/send_report/$', views.send_report, name='send_report'),
    url(r'^profile/edit_report/(?P<pk>[0-9]+)/$', views.edit_report, name='edit_report'),
]
