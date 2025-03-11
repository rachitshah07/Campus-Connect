from django.shortcuts import render, redirect, HttpResponse
from core.EmailBackend import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from core.models import CustomUser
from django.contrib.auth.decorators import login_required

# Create your views here.

def BASE(request):
    return render(request, "base.html")


def LOGIN(request):
    return render(request, "login.html")


def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(email, password)
        if user != None:
            login(request, user)
            user_type = user.user_type
            if (user_type == "1"):
                return redirect("hod_home")
            elif (user_type == "2"):
                return redirect("staff_home")
            elif (user_type == "3"):
                return redirect("student_home")
            else:
                messages.error(request, "Email or Password Incorrect!!")
                return redirect('login')
        else:
            messages.error(request, "Email or Password Incorrect!!")
            return redirect('login')
    return HttpResponse("This is get ")


def doLogout(request):
    logout(request)
    return redirect("login")


@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request, "profile.html", context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        # email=request.POST.get("email")
        # username=request.POST.get("username")
        password = request.POST.get("password")

        print(profile_pic)

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            # customuser.profile_pic=profile_pics

            if password not in [None, ""]:
                customuser.set_password(password)
            if profile_pic not in [None, ""]:
                customuser.profile_pic = profile_pic

            customuser.save()
            messages.success(request, "Profile Updation Succeded!!")
            return redirect("profile")
        except Exception:
            messages.error(request, "Profile Updation Failed")
            return redirect("profile")
    return render(request, "profile.html")
