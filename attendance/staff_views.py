from django.shortcuts import render, redirect
from app.models import Session_Year,Staff,Staff_Notification,Student, StudentResult,Subject,Staff_Leave, Staff_Feedback, Attendance,Attendance_Report
from django.contrib import messages

def home(request):
    return render(request, 'staff/home.html')

def notification(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        print(i.id)
        notification = Staff_Notification.objects.filter(staff_id = staff_id)

        context = {
            'notification' : notification,
        }
        return render(request, 'staff/notification.html', context)
    
def mark_as_done(request, status):
    notification = Staff_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('staff_notification')

def staff_leave(request):

    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_Leave.objects.filter(staff_id = staff_id)

        context = {
            'staff_leave_history':staff_leave_history,
        }
    return render(request, 'staff/staff_leave.html', context)

def staff_leave_save(request):
    if request.method == "POST":
        date = request.POST.get('date')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin=request.user.id)

        leave = Staff_Leave(
            staff_id = staff,
            data = date,
            message = message,
        )

        leave.save()
        messages.success(request, 'Leave Applied Successfully')
        return redirect('staff_leave')
    return render(request, 'staff/staff_leave.html')    

def staff_feedback(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    
    staff_feedback_history = Staff_Feedback.objects.filter(staff_id = staff_id)

    context = {
        'staff_feedback_history':staff_feedback_history,
    }
    return render(request, 'staff/staff_feedback.html', context)

def staff_feedback_save(request):
    if request.method == "POST":
        message = request.POST.get('message')

        staff = Staff.objects.get(admin=request.user.id)
        
        feedback = Staff_Feedback(
            staff_id = staff,
            feedback = message,
            feedback_reply=""
        )

        feedback.save()
        messages.success(request, 'Feedback Sent Successfully')
        return redirect('staff_feedback_save')
    return render(request, 'staff/staff_feedback.html')

def staff_take_attendance(request):
    get_subject = None
    get_session_year = None
    students=None
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff = staff_id)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subject.objects.get(id = subject_id) 
            get_session_year = Session_Year.objects.get(id = session_year_id) 

            subject = Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id = i.course.id
                students = Student.objects.filter(course_id = student_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'action':action,
        'students':students,
    }
    return render(request, 'staff/take_attendance.html', context)

def staff_save_attendance(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id =get_subject,
            attendance_date=attendance_date,
            session_year_id=get_session_year,
        )
        attendance.save()

        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)
            print(stud_id)
            print(i)
            p_students = Student.objects.get(id = int_stud)

            attendance_report = Attendance_Report(
                student_id = p_students,
                attendance_id = attendance,
            )

            attendance_report.save()
            messages.success(request, 'Attendance Recorded Successfully')
    return redirect('staff_take_attendance')

def staff_view_attendance(request):
    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff_id =staff_id)
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
    return render(request, 'staff/view_attendance.html', context)
    
def STAFF_ADD_RESULT(request):
    staff = Staff.objects.get(admin=request.user.id)

    subjects = Subject.objects.filter(staff_id = staff)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    students = None
    if action is not None:
        if request.method == "POST":
           subject_id = request.POST.get('subject_id')
           session_year_id = request.POST.get('session_year_id')

           get_subject = Subject.objects.get(id = subject_id)
           get_session = Session_Year.objects.get(id = session_year_id)

           subjects = Subject.objects.filter(id = subject_id)
           for i in subjects:
               student_id = i.course.id
               students = Student.objects.filter(course_id = student_id)


    context = {
        'subjects':subjects,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session':get_session,
        'students':students,
    }

    return render(request,'staff/add_result.html',context)


def STAFF_SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        Exam_mark = request.POST.get('Exam_mark')

        get_student = Student.objects.get(admin = student_id)
        get_subject = Subject.objects.get(id=subject_id)

        check_exist = StudentResult.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=get_subject, student_id=get_student)
            result.assignment_mark = assignment_mark
            result.exam_mark = Exam_mark
            result.save()
            messages.success(request, "Successfully Updated Result")
            return redirect('staff_add_result')
        else:
            result = StudentResult(student_id=get_student, subject_id=get_subject, exam_mark=Exam_mark,
                                   assignment_mark=assignment_mark)
            result.save()
            messages.success(request, "Successfully Added Result")
            return redirect('staff_add_result')