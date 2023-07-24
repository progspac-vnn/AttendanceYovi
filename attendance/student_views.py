from django.shortcuts import render, redirect
from app.models import Session_Year,Staff,Staff_Notification,Student,Subject,Staff_Leave, Staff_Feedback, StudentResult,Student_Feedback, Student_Notification, Student_Leave, Attendance, Attendance_Report
from django.contrib import messages

def home(request):
    return render(request, 'student/home.html')

def notification(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        print(i.id)
        notification = Student_Notification.objects.filter(student_id = student_id)

        context = {
            'notification' : notification,
        }
        return render(request, 'student/notification.html', context)

def mark_as_done(request, status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')


def student_leave(request):

    student = Student.objects.filter(admin=request.user.id)
    for i in student:
        student_id = i.id
        student_leave_history = Student_Leave.objects.filter(student_id = student_id)

        context = {
            'student_leave_history':student_leave_history,
        }
    return render(request, 'student/student_leave.html', context)

def student_leave_save(request):
    if request.method == "POST":
        date = request.POST.get('date')
        message = request.POST.get('message')

        student = Student.objects.get(admin=request.user.id)

        leave = Student_Leave(
            student_id = student,
            data = date,
            message = message,
        )

        leave.save()
        messages.success(request, 'Leave Applied Successfully')
        return redirect('student_leave')
    return render(request, 'student/student_leave.html')    

def student_feedback(request):
    student_id = Student.objects.get(admin=request.user.id)
    
    student_feedback_history = Student_Feedback.objects.filter(student_id = student_id)

    context = {
        'student_feedback_history':student_feedback_history,
    }
    return render(request, 'student/student_feedback.html', context)

def student_feedback_save(request):
    if request.method == "POST":
        message = request.POST.get('message')

        student = Student.objects.get(admin=request.user.id)
        
        feedback = Student_Feedback(
            student_id = student,
            feedback = message,
            feedback_reply=""
        )

        feedback.save()
        messages.success(request, 'Feedback Sent Successfully')
        return redirect('student_feedback_save')
    return render(request, 'student/student_feedback.html')

def  student_view_attendance(request):

    student = Student.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(course=student.course_id)
    action = request.GET.get('action')
    get_subject = None 
    attendance_report = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)
            attendance_report = Attendance_Report.objects.filter(student_id=student, attendance_id__subject_id = subject_id)

    context = {
        'subjects': subjects,
        'action': action,
        'get_subject':get_subject,
        'attendance_report': attendance_report,
    }

    return render(request, 'student/view_attendance.html', context)

def student_view_result(request):
    student = Student.objects.get(admin=request.user.id)
    result = StudentResult.objects.filter(student_id = student)
    mark = None 

    for i in result:
        assignment_mark = i.assignment_mark 
        exam_mark = i.exam_mark

        mark = assignment_mark + exam_mark

    context = {
        'result':result,
        'mark': mark,
    }
    return render(request, 'student/view_result.html', context)