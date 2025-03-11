from django.shortcuts import render, redirect
from core.models import  Student_Notification, Student, Student_Feedback, Student_Leave, Student_Result, Subject, Attendance, Attendance_Report
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib import colors

def Home(request):
    return render(request, "student/home.html")

def STUDENT_NOTIFICATION(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        print(i)
        student_id = i.id
        notification = Student_Notification.objects.filter(student_id = student_id)

        context = {
            'notification' : notification
        }
    return render(request, 'student/notification.html', context)

def STUDENT_NOTIFICATION_MARK_AS_DONE(request, status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')

def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin = request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id = student_id)

    context = {
        'feedback_history' : feedback_history
    }
    return render(request, 'student/feedback.html', context)

def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        student = Student.objects.get(admin = request.user.id)
        feedbacks = Student_Feedback(
            student_id = student,
            feedback = feedback,
            feedback_reply = ""
        )
        feedbacks.save()
        return redirect('student_feedback')

def STUDENT_LEAVE(request):
    student = Student.objects.get(admin=request.user.id)
    student_leave_history = Student_Leave.objects.filter(student_id=student)

    context = {
        'student_leave_history' : student_leave_history
    }

    return render(request, 'student/apply_for_leave.html', context)

def STUDENT_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_id = Student.objects.get( admin = request.user.id )
        student_leave = Student_Leave(
            student_id = student_id,
            date = leave_date,
            message = leave_message
        ) 
        student_leave.save()
        messages.success(request, "Leave requested successfully!")
        return redirect('student_leave')
    
def STUDENT_VIEW_ATTENDANCE(request):
    student = Student.objects.get(admin = request.user.id)
    subjects = Subject.objects.filter(course = student.course_id)

    action = request.GET.get('action')
    get_subject = None
    attendance = None
    attendance_report = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id = subject_id)
            
            attendance_report = Attendance_Report.objects.filter(student_id= student, attendance_id__subject_id = subject_id)

    context = {
        'subjects':subjects,
        'action' : action,
        'get_subject' : get_subject,
        'attendance_report' : attendance_report
    }
    return render(request, 'student/view_attendance.html', context)

def STUDENT_VIEW_RESULT(request):
    student = Student.objects.get(admin = request.user.id)

    total = None
    result = Student_Result.objects.filter(student_id = student)
    for i in result:
        assignment_mark = i.assignment_mark
        practical_mark = i.practical_mark
        ce_mark = i.ce_mark
        lpw_mark = i.lpw_mark
        see_mark = i.see_mark

        total = (ce_mark + assignment_mark)*0.4 + (practical_mark*0.75 + lpw_mark)*0.2 + see_mark*0.4
        total = int(total)
    context = {
        'result' : result,
        'total' : total
    }

    return render(request, 'student/view_result.html', context)


def STUDENT_DOWNLOAD_RESULT(request):
    buf = io.BytesIO()
    
    doc = SimpleDocTemplate(buf, pagesize=A4)
    elements = []

    students = Student.objects.get(admin = request.user.id) 
    student_name = f"{students.admin.first_name} {students.admin.last_name}"
    
    header_text = f"Result of {student_name}"
    
    data = []
    table_header = ["Subject", "CE Component", "Assignment", "Practical", "LPW", "SEE", "Status"]
    data.append(table_header)
    results = Student_Result.objects.filter(student_id=students)
        
    
    for result in results:

        subject_name = result.subject_id.name
        ce_marks = f"{result.ce_mark} / 70"
        assignment_marks = f"{result.assignment_mark} / 30"
        practical_marks = f"{result.practical_mark} / 100"
        lpw_marks = f"{result.lpw_mark} / 25"
        see_marks = f"{result.see_mark} / 100"
        total = (result.ce_mark + result.assignment_mark) * 0.4 + (result.practical_mark * 0.75 + result.lpw_mark) * 0.2 + result.see_mark * 0.4
        status = "PASS" if total >= 40 else "FAIL"

        row = [subject_name, ce_marks, assignment_marks, practical_marks, lpw_marks, see_marks, status]
        data.append(row)

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)

    # Set the buffer position to the beginning
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='Results.pdf')