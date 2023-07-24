from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Course, Session_Year, customUser, Student, Staff, Subject, Session_Year, Student_Feedback,Staff_Notification, Staff_Leave, Staff_Feedback, Student_Notification, Student_Leave, Attendance_Report, Attendance
from django.contrib import messages

@login_required(login_url='/')
def home(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender = 'Male').count()
    student_gender_female = Student.objects.filter(gender = 'Female').count()



    context = {
        'student_count' : student_count,
        'staff_count' : staff_count,
        'course_count' : course_count,
        'subject_count' : subject_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
    }

    return render(request, 'hod/home.html', context)

@login_required(login_url='/')
def add_student(request):

    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        passw = request.POST.get('passw')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        
        if customUser.objects.filter(email = email).exists():
            messages.warning(request, 'This Email is already in use')
            return redirect('add_student')
        if customUser.objects.filter(username = username).exists():
            messages.warning(request, 'This username is already in use')
            return redirect('add_student')
        else:
            user = customUser(
                first_name=first_name,
                last_name=last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3,
            )

            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            user.set_password(passw)
            user.save()

            student = Student(
                admin = user,
                address = address,
                Session_Year_id = session_year,
                course_id = course,
                gender = gender,
            )
            student.save()
            messages.success(request, 'Student' + first_name + " " + last_name + " added successfully")
            return redirect('add_student')
            
    context = {
        'course': course,
        'session_year': session_year
    }
    return render(request, 'hod/add_student.html', context)

def view_student(request):

    student = Student.objects.all()

    context = {
        'student': student
    }
    return render(request, 'hod/view_student.html', context)

def edit_student(request, id):
    student = Student.objects.filter(id = id) 
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    context = {
        'student' : student,
        'course' : course,
        'session_year' : session_year,
    }
    return render(request, 'hod/edit_student.html', context)

def update_student(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        passw = request.POST.get('passw')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = customUser.objects.get(id = student_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        student = Student.objects.get(admin = student_id)
        student.address = address
        student.gender = gender

        if passw != None and passw != "":
                user.set_password(passw)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic

        course = Course.objects.get(id=course_id)
        student.course_id = course

        session_year = Session_Year.objects.get(id=session_year_id)
        student.Session_Year_id = session_year

        student.save()
        messages.success(request, 'Records Are Successfully Updated')
        return redirect('view_student')

    return render(request, 'hod/edit_student.html')

def delete_student(request, admin):
    student = customUser.objects.get(id = admin)
    student.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('view_student')

def add_course(request):

    if request.method == 'POST':

        course_name = request.POST.get('course_name')
        print(course_name)

        course = Course(
            name=course_name
        )
        course.save()
        messages.success(request, 'Course Added Successfully')
        return redirect('add_course')
    
    return render(request, 'hod/add_course.html')

def view_course(request):

    course = Course.objects.all()
    
    context = {
        'course' : course
    }

    return render(request, 'hod/view_course.html', context)

def edit_course(request, id):
    course = Course.objects.get(id = id)
    
    context = {
        'course': course,
    }

    return render(request, 'hod/edit_course.html', context)

def update_course(request):
    if request.method == 'POST':
        name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')

        course = Course.objects.get(id=course_id)
        course.name = name
        course.save()
        messages.success(request, "Course Updated Successfully")
        return redirect('view_course')
    return render(request, 'hod/edit_course.html')

def delete_course(request, id):
    course = Course.objects.get(id = id)
    course.delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('view_course')


# STAFF
@login_required(login_url='/')
def add_staff(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        passw = request.POST.get('passw')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if customUser.objects.filter(email = email).exists():
            messages.warning(request, 'This Email is already in use')
            return redirect('add_staff')
        if customUser.objects.filter(username = username).exists():
            messages.warning(request, 'This username is already in use')
            return redirect('add_staff')
        else:
            user = customUser(
                first_name=first_name,
                last_name=last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 2,
            )

            user.set_password(passw)
            user.save()
     
            staff = Staff(
                admin = user,
                address = address,
                gender = gender,
            )
            staff.save()
            messages.success(request, 'Staff' + first_name + " " + last_name + " added successfully")
            return redirect('add_staff')
            
    
    return render(request, 'hod/add_staff.html') 
def view_staff(request):
    staff = Staff.objects.all()

    context = {
        'staff': staff
    }
    return render(request, 'hod/view_staff.html', context)

def edit_staff(request, id):
    staff = Staff.objects.get(id = id)

    context = {
        'staff':staff
    }
    return render(request, 'hod/edit_staff.html', context)

def update_staff(request):

    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        passw = request.POST.get('passw')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = customUser.objects.get(id=staff_id)
        
        user.profile_pic = profile_pic
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        user.set_password(passw)
        user.save()

        if passw != None and passw != "":
                user.set_password(passw)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic

        staff = Staff.objects.get(id=staff_id)
        staff.address = address
        staff.gender = gender
        
        staff.save()
        messages.success(request, 'Records Are Successfully Updated')
        return redirect('view_staff')

    return render(request, 'hod/view_staff.html')

def delete_staff(request, id):
    staff = Staff.objects.get(id = id)
    staff.delete()
    messages.success(request, 'Staff deleted successfully')
    return redirect('view_staff')

# Subject

def add_subject(request):
    course = Course.objects.all()
    staff = Staff.objects.all()

    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id') 
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)

        subject = Subject(
            name = subject_name,
            course = course, 
            staff = staff
        )

        subject.save()
        messages.success(request, 'Subject added successfully')
        return redirect('add_subject')

    context = {
        'course' : course,
        'staff' : staff
    }
    return render(request, 'hod/add_subject.html', context)

def view_subject(request):

    subject = Subject.objects.all()

    context = {
        'subject': subject
    }

    return render(request, 'hod/view_subject.html', context)

def edit_subject(request, id):
    subject = Subject.objects.get(id = id)
    course = Course.objects.all()
    staff = Staff.objects.all()

    context = {
        'subject' : subject,
        'course' : course,
        'staff' : staff,
    }

    return render(request, 'hod/edit_subject.html', context)

def update_subject(request):
    
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        subject_id = request.POST.get('subject_id')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        
        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)

        subject = Subject(
            id = subject_id,
            name = subject_name,
            course = course,
            staff = staff,
        )
        subject.save()
        messages.success(request, 'Subject Changed Successfully')
        return redirect('view_subject')
    return render(request, 'hod/view_subject.html')

def delete_subject(request, id):
    subject = Subject.objects.get(id = id)
    subject.delete()
    messages.success(request, 'Staff deleted successfully')
    return redirect('view_subject')

# Session

def add_session(request):
    if request.method == 'POST':
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session_year = Session_Year(
            session_start = session_year_start,
            session_end = session_year_end
        )

        session_year.save()

        messages.success(request, 'session created successfully')
        return redirect('add_session')

    return render(request, 'hod/add_session.html')

def view_session(request):

    session = Session_Year.objects.all()

    context = {
        'session': session
    }

    return render(request, 'hod/view_session.html', context)

def edit_session(request, id):
    session = Subject.objects.get(id = id)
    context = {
        'session' : session
    }

    return render(request, 'hod/edit_session.html', context)

def update_session(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year.objects.get(id=session_id)
        session.session_start = session_year_start
        session.session_end = session_year_end
        
        session.save()
        messages.success(request, 'Records Are Successfully Updated')
        return redirect('view_session')

    return render(request, 'hod/view_session.html')

def delete_session(request, id):
    session = Session_Year.objects.get(id = id)
    session.delete()
    messages.success(request, 'Session deleted successfully')
    return redirect('view_session')

def staff_send_notification(request):

    staff = Staff.objects.all()
    
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'staff' : staff,
        'see_notification' : see_notification,
    }
    return render(request, 'hod/staff_send_notification.html', context)

def staff_save_notification(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin=staff_id)
        notification = Staff_Notification(
            staff_id = staff,
            message = message
        )

        notification.save()
        messages.success(request, 'Notification Sent Successfully')
        return redirect('staff_send_notification')
    return render(request, 'hod/staff_send_notification.html')

def staff_leave_view(request):
    leave = Staff_Leave.objects.all()
    context = {
        'leave': leave, 
    }
    return render(request, 'hod/staff_leave_view.html',context)

def staff_leave_approve(request, id):
    leave = Staff_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')    


def staff_leave_disapprove(request, id):
    leave = Staff_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')

def staff_feedback_reply(request):
    feedback = Staff_Feedback.objects.all()

    context = {
        'feedback':feedback,
    }
    return render(request, 'hod/staff_send_feedback_reply.html', context)

def staff_feedback_reply_save(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback')
        print(feedback_id)

        hod_feedback = Staff_Feedback.objects.get(id = feedback_id)
        hod_feedback.feedback_reply = feedback_reply

        hod_feedback.save()
        messages.success(request, 'Reply Sent Successfully')
        return redirect('staff_feedback_reply')
    return render(request, 'hod/staff_send_feedback_reply.html')


# Student
def student_send_notification(request):
    student = Student.objects.all()
    
    see_notification = Student_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'student' : student,
        'see_notification' : see_notification,
    }
    return render(request, 'hod/student_send_notification.html', context)

def student_save_notification(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')

        student = Student.objects.get(admin=student_id)
        notification = Student_Notification(
            student_id = student,
            message = message
        )

        notification.save()
        messages.success(request, 'Notification Sent Successfully')
        return redirect('student_send_notification')
    return render(request, 'hod/student_send_notification.html')

def student_leave_view(request):
    leave = Student_Leave.objects.all()
    context = {
        'leave': leave, 
    }
    return render(request, 'hod/student_leave_view.html',context)

def student_leave_approve(request, id):
    leave = Student_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('student_leave_view')    


def student_leave_disapprove(request, id):
    leave = Student_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('student_leave_view')

def student_feedback_reply(request):
    feedback = Student_Feedback.objects.all()

    context = {
        'feedback':feedback,
    }
    return render(request, 'hod/student_send_feedback_reply.html', context)

def student_feedback_reply_save(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback')
        print(feedback_id)

        hod_feedback = Student_Feedback.objects.get(id = feedback_id)
        hod_feedback.feedback_reply = feedback_reply

        hod_feedback.save()
        messages.success(request, 'Reply Sent Successfully')
        return redirect('student_feedback_reply')
    return render(request, 'hod/student_send_feedback_reply.html')

def view_attendance(request):
    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None
    subject = Subject.objects.all()
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subject.objects.get(id = subject_id) 
            get_session_year = Subject.objects.get(id = session_year_id) 
            attendance = Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date)

            subject = Subject.objects.filter(id=subject_id)
            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'action':action,
        'attendance_date':attendance_date, 
        'attendance_report':attendance_report,
    }
    
    return render(request, 'hod/view_attendance.html', context)