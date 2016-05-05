from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^professor/(?P<pk>[0-9]+)/$', views.DetailProfessorView.as_view(), name='professor_detail'),
    url(r'^student/(?P<pk>[0-9]+)/$', views.DetailStudentView.as_view(), name='student_detail'),
    url(r'^profile/$', views.profile_view, name='profile_view'),
    url(r'^profile/professor/$', views.ProfileProfessorView.as_view(), name='profile_professor_view'),
    # Reports change
    url(r'^profile/change_report/$', views.ReportChangeView.as_view(), name='report_change'),
    url(r'^profile/send_report/$', views.send_report, name='send_report'),
    url(r'^profile/edit_report/(?P<pk>[0-9]+)/$', views.edit_report, name='edit_report'),
    url(r'^profile/delete_report/(?P<pk>[0-9]+)/$', views.delete_report, name='delete_report'),
    # Meetings change
    url(r'^profile/change_meeting/$', views.MeetingChangeView.as_view(), name='meeting_change'),
    url(r'^profile/send_meeting/$', views.send_meeting, name='send_meeting'),
    url(r'^profile/edit_meeting/(?P<pk>[0-9]+)/$', views.edit_meeting, name='edit_meeting'),
    url(r'^profile/delete_meeting/(?P<pk>[0-9]+)/$', views.delete_meeting, name='delete_meeting'),
    # Students change
    url(r'^profile/change_student/$', views.StudentChangeView.as_view(), name='student_change'),
    url(r'^profile/send_student/$', views.send_student, name='send_student'),
    url(r'^profile/edit_student/(?P<pk>[0-9]+)/$', views.edit_student, name='edit_student'),
    url(r'^profile/delete_student/(?P<pk>[0-9]+)/$', views.delete_student, name='delete_student'),
]
