from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import hod_views, staff_views, student_views, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base, name='base'),

     #Login path
    path('', views.loginpage, name='loginpage'), 
    path('doLogin/', views.doLogin, name='doLogin'),
    path('doLogout/', views.doLogout, name='logout'),

    # Profile update
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),

    # HOD Panel Url
    path('hod/home', hod_views.home, name='hod_home'),
        # Student
    path('hod/student/add', hod_views.add_student, name='add_student'),
    path('hod/student/view', hod_views.view_student, name='view_student'),
    path('hod/student/edit/<str:id>', hod_views.edit_student, name='edit_student'),
    path('hod/student/update', hod_views.update_student, name="update_student"),
    path('hod/student/delete/<str:admin>', hod_views.delete_student, name="delete_student"),
    path('hod/student/leave_view', hod_views.student_leave_view, name="student_leave_view"),
    path('hod/student/leave/approve/<str:id>', hod_views.student_leave_approve, name="student_leave_approve"),
    path('hod/student/leave/disapprove/<str:id>', hod_views.student_leave_disapprove, name="student_leave_disapprove"),
    path('hod/student/feedback/reply', hod_views.student_feedback_reply, name="student_feedback_reply"),
    path('hod/student/feedback_reply/save', hod_views.student_feedback_reply_save, name="student_feedback_save_reply"),

    path('hod/view/attendance', hod_views.view_attendance, name="view_attendance"),
    



        # Staff
    path('hod/staff/add', hod_views.add_staff, name='add_staff'),
    path('hod/staff/view', hod_views.view_staff, name='view_staff'),
    path('hod/staff/edit/<str:id>', hod_views.edit_staff, name="edit_staff"),
    path('hod/staff/update', hod_views.update_staff, name="update_staff"),
    path('hod/staff/delete/<str:id>', hod_views.delete_staff, name="delete_staff"),
    path('hod/staff/leave_view', hod_views.staff_leave_view, name="staff_leave_view"),
    path('hod/staff/leave/approve/<str:id>', hod_views.staff_leave_approve, name="staff_leave_approve"),
    path('hod/staff/leave/disapprove/<str:id>', hod_views.staff_leave_disapprove, name="staff_leave_disapprove"),
    path('hod/staff/feedback/reply', hod_views.staff_feedback_reply, name="staff_feedback_reply"),
    path('hod/staff/feedback_reply/save', hod_views.staff_feedback_reply_save, name="staff_feedback_save_reply"),

        # Subject
    path('hod/subject/add', hod_views.add_subject, name='add_subject'),
    path('hod/subject/view', hod_views.view_subject, name='view_subject'),
    path('hod/subject/edit/<str:id>', hod_views.edit_subject, name="edit_subject"),
    path('hod/subject/update', hod_views.update_subject, name="update_subject"),
    path('hod/subject/delete/<str:id>', hod_views.delete_subject, name="delete_subject"), 

        # Session
    path('hod/session/add', hod_views.add_session, name='add_session'),
    path('hod/session/view', hod_views.view_session, name='view_session'),
    path('hod/session/edit/<str:id>', hod_views.edit_session, name="edit_session"),
    path('hod/session/update', hod_views.update_session, name="update_session"),
    path('hod/session/delete/<str:id>', hod_views.delete_session, name="delete_session"), 

        #Course
    path('hod/course/add', hod_views.add_course, name="add_course"),
    path('hod/course/view', hod_views.view_course, name="view_course"),
    path('hod/course/edit/<str:id>', hod_views.edit_course, name="edit_course"),
    path('hod/course/update', hod_views.update_course, name="update_course"),
    path('hod/course/delete/<str:id>', hod_views.delete_course, name="delete_course"),

        # Staff Notification
    path('hod/staff/send_notification', hod_views.staff_send_notification, name="staff_send_notification"),
    path('hod/staff/save_notification', hod_views.staff_save_notification, name="staff_save_notification"),

        # Student Notification
    path('hod/student/send_notification', hod_views.student_send_notification, name="student_send_notification"),
    path('hod/student/save_notification', hod_views.student_save_notification, name="student_save_notification"),   

    # Staff
    path('staff/home', staff_views.home, name='staff_home'),
    path('staff/notification', staff_views.notification, name='staff_notification'),
    path('staff/leave', staff_views.staff_leave, name='staff_leave'),
    path('staff/mark_as_done/<str:status>', staff_views.mark_as_done, name='staff_mark_as_done'),
    path('staff/leave_save', staff_views.staff_leave_save, name='staff_leave_save'),
    path('staff/feedback', staff_views.staff_feedback, name='staff_feedback'),
    path('staff/feedback/save', staff_views.staff_feedback_save, name='staff_feedback_save'),
    path('staff/take_attendance', staff_views.staff_take_attendance, name="staff_take_attendance"),
    path('staff/save_attendance', staff_views.staff_save_attendance, name="staff_save_attendance"),
    path('staff/view_attendance', staff_views.staff_view_attendance, name="staff_view_attendance"),
    path('staff/result/add', staff_views.STAFF_ADD_RESULT, name="staff_add_result"),
    path('staff/result/save', staff_views.STAFF_SAVE_RESULT, name="staff_save_result"),




    # Student
    path('student/home', student_views.home, name="student_home"),
    path('student/notification', student_views.notification, name='student_notification'),
    path('student/mark_as_done/<str:status>', student_views.mark_as_done, name='student_mark_as_done'),
    path('student/leave', student_views.student_leave, name='student_leave'),
    path('student/leave_save', student_views.student_leave_save, name='student_leave_save'),
    path('student/feedback', student_views.student_feedback, name='student_feedback'),
    path('student/feedback/save', student_views.student_feedback_save, name='student_feedback_save'),
    path('student/view_attendance', student_views.student_view_attendance, name='student_view_attendance'),
    path('student/view_result', student_views.student_view_result, name='student_view_result'),
    


] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)