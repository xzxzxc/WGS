from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^professor/(?P<pk>[0-9]+)/$', views.DetailProfessorView.as_view(), name='professor_detail'),
    url(r'^student/(?P<pk>[0-9]+)/$', views.DetailStudentView.as_view(), name='student_detail'),
    url(r'^profile/$', views.profile_view, name='profile_view'),
    url(r'^profile/professor/$', views.ProfileProfessorView.as_view(), name='professor_profile'),
    url(r'^profile/student/$', views.ProfileStudentView.as_view(), name='student_profile'),
    # Meetings change
    url(r'^profile/change_meeting/$', views.MeetingChangeView.as_view(), name='meeting_change'),
    url(r'^profile/send_meeting/$', views.send_meeting, name='send_meeting'),
    url(r'^profile/edit_meeting/(?P<pk>[0-9]+)/$', views.edit_meeting, name='edit_meeting'),
    url(r'^profile/delete_meeting/(?P<pk>[0-9]+)/$', views.delete_meeting, name='delete_meeting'),
    # Reports change
    # url(r'^profile/meeting/(?P<meeting_pk>[0-9]+)/change_report/$', views.ReportChangeView.as_view(), name='report_change'),
    url(r'^profile/meeting/(?P<meeting_pk>[0-9]+)/add_report/$', views.add_report, name='add_report'),
    url(r'^profile/meeting/(?P<meeting_pk>[0-9]+)/edit_report/(?P<pk>[0-9]+)/$', views.edit_report, name='edit_report'),
    url(r'^profile/meeting/(?P<meeting_pk>[0-9]+)/delete_report/(?P<pk>[0-9]+)/$', views.delete_report, name='delete_report'),
    # Files change
    url(r'^profile/change_file$', views.FileChangeView.as_view(), name='file_change'),
    url(r'^profile/attach_file/(?P<pk>[0-9]+)/$', views.attach_file, name='attach_file'),
    # Students change
    url(r'^profile/change_student/$', views.StudentChangeView.as_view(), name='student_change'),
    url(r'^profile/send_student/$', views.send_student, name='send_student'),
    url(r'^profile/edit_student/(?P<pk>[0-9]+)/$', views.edit_student, name='edit_student'),
    url(r'^profile/delete_student/(?P<pk>[0-9]+)/$', views.delete_student, name='delete_student'),
    # Dirs change
    url(r'^profile/change_dir/$', views.DirChangeView.as_view(), name='dir_change'),
    url(r'^profile/send_dir/$', views.send_dir, name='send_dir'),
    url(r'^profile/edit_dir/(?P<pk>[0-9]+)/$', views.edit_dir, name='edit_dir'),
    url(r'^profile/delete_dir/(?P<pk>[0-9]+)/$', views.delete_dir, name='delete_dir'),
    url(r'^profile/delete_file/(?P<pk>[0-9]+)/$', views.delete_file, name='delete_file'),
    # Professor profile change
    url(r'^profile/professor/edit/$', views.edit_professor_profile, name='edit_professor_profile'),
    # Student profile change
    url(r'^student/edit_profile/$', views.edit_student_profile, name='edit_student_profile'),
]
