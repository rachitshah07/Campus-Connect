from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from core.models import (
    Session_Year,
    Course,
    CustomUser,
    Student,
    Staff,
    Student_Result,
    Subject,
    Staff_Notification,
    Staff_Leave,
    Staff_Feedback,
    Attendance_Report,
    Attendance,
)
from django.contrib import messages


@login_required(login_url="/")
def HOME(request):
    return render(request, "staff/home.html")


@login_required(login_url="/")
def NOTIFICATION(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
    notification = Staff_Notification.objects.filter(staff_id=staff_id)
    context = {"notification": notification}
    return render(request, "staff/notification.html", context)


@login_required(login_url="/")
def STAFF_NOTIFICATION_MARK_AS_DONE(request, status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect("notifications")


@login_required(login_url="/")
def STAFF_APPLY_LEAVE(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
    staff_leave_history = Staff_Leave.objects.filter(staff_id=staff_id)
    context = {"staff_leave_history": staff_leave_history}

    return render(request, "staff/apply_leave.html", context)


@login_required(login_url="/")
def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message")
        staff = Staff.objects.get(admin=request.user.id)

        leave = Staff_Leave(
            staff_id=staff,
            date=leave_date,
            message=leave_message,
        )
        messages.success(request, "Leave Sent Successfully!")
        leave.save()
        return redirect("staff_apply_leave")
    return redirect("staff_apply_leave")


def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    feedback_history = Staff_Feedback.objects.filter(staff_id=staff_id)

    context = {
        "feedback_history": feedback_history,
    }

    return render(request, "staff/feedback.html", context)


def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get("feedback")
        staff = Staff.objects.get(admin=request.user.id)

        feedback = Staff_Feedback(staff_id=staff, feedback=feedback, feedback_reply="")
        feedback.save()
        return redirect("staff_feedback")


def STAFF_TAKE_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin=request.user.id)

    subject = Subject.objects.filter(staff=staff_id)
    session_year = Session_Year.objects.all()

    action = request.GET.get("action")

    get_subject = None
    get_session_year = None
    students = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get("subject_id")
            session_year_id = request.POST.get("session_year_id")

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)

            subject = Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)
    context = {
        "subject": subject,
        "session_year": session_year,
        "get_subject": get_subject,
        "get_session_year": get_session_year,
        "action": action,
        "students": students,
    }

    return render(request, "staff/take_attendance.html", context)


def STAFF_SAVE_ATTENDANCE(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        session_year_id = request.POST.get("session_year_id")
        attendance_date = request.POST.get("attendance_date")
        student_id = request.POST.getlist("student_id")
        print(student_id)

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id=get_subject,
            attendance_date=attendance_date,
            session_year_id=get_session_year,
        )
        attendance.save()

        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)

            p_students = Student.objects.get(id=int_stud)
            attendance_report = Attendance_Report(
                student_id=p_students, attendance_id=attendance
            )
            attendance_report.save()

    return redirect("staff_take_attendance")

def STAFF_VIEW_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    subject = Subject.objects.filter(staff_id = staff_id)
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report =None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subject.objects.get(id = subject_id)
            get_session_year = Session_Year.objects.get(id = session_year_id)
            attendance = Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)

    context = {
        'subject':subject,
        'session_year' : session_year,
        'action':action,
        'get_subject' : get_subject,
        'get_session_year' : get_session_year,
        'attendance_date' : attendance_date,
        'attendance_report' : attendance_report

    }
    return render(request, 'staff/view_attendance.html', context)

def STAFF_ADD_RESULT(request):
    staff = Staff.objects.get(admin = request.user.id)
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

    return render(request,'Staff/add_result.html',context)


def STAFF_SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        ce_mark = request.POST.get('ce_mark')
        practical_mark = request.POST.get('practical_mark')
        lpw_mark = request.POST.get('lpw_mark')
        see_mark = request.POST.get('see_mark')

        get_student= None   
        get_subject = None

        get_student = Student.objects.get(admin = student_id)
        get_subject = Subject.objects.get(id = subject_id)

        check_exist = Student_Result.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exist:
            result = Student_Result.objects.get(subject_id=get_subject, student_id=get_student)
            result.assignment_mark = assignment_mark
            result.practical_mark = practical_mark
            result.ce_mark = ce_mark
            result.lpw_mark = lpw_mark
            result.see_mark = see_mark
           
            result.save()
            messages.success(request, "Result Updated Successfully!")
            return redirect('staff_add_result')
        else:
            result = Student_Result(
                student_id=get_student, 
                subject_id=get_subject, 
                assignment_mark=assignment_mark,
                ce_mark=ce_mark,
                practical_mark = practical_mark,
                lpw_mark=lpw_mark, 
                see_mark=see_mark
            )
            result.save()
            messages.success(request, "Result Added Successfully!")
            return redirect('staff_add_result')