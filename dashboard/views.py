from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, Course, Enrollment, Grade


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")


@login_required(login_url='login')
def dashboard(request):
    return render(request, "dashboard.html")


@login_required(login_url='login')
def profile(request):
    profile, _ = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.username,
            "age": 18,
            "course": "Not Assigned"
        }
    )

    return render(request, "profile.html", {"profile": profile})


@login_required(login_url='login')
def courses(request):
    profile, _ = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.username,
            "age": 18,
            "course": "Not Assigned"
        }
    )

    all_courses = Course.objects.all()
    enrolled = Enrollment.objects.filter(student=profile).values_list("course_id", flat=True)

    if request.method == "POST":
        course_id = request.POST.get("course_id")
        course = Course.objects.get(id=course_id)
        Enrollment.objects.get_or_create(student=profile, course=course)
        return redirect("courses")

    return render(request, "courses.html", {
        "courses": all_courses,
        "enrolled": enrolled
    })


@login_required(login_url='login')
def grades_dashboard(request):
    profile, _ = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.username,
            "age": 18,
            "course": "Not Assigned"
        }
    )

    enrollments = Enrollment.objects.filter(student=profile)
    grades = Grade.objects.filter(enrollment__in=enrollments)

    return render(request, "grades.html", {"grades": grades})


@login_required(login_url='login')
def gpa_dashboard(request):
    profile, _ = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.username,
            "age": 18,
            "course": "Not Assigned"
        }
    )

    enrollments = Enrollment.objects.filter(student=profile)
    grades = Grade.objects.filter(enrollment__in=enrollments)

    total_score = 0
    count = 0

    for g in grades:
        total_score += g.score
        count += 1

    if count > 0:
        gpa = round(total_score / count / 10, 2)
    else:
        gpa = 0

    return render(request, "gpa.html", {
        "grades": grades,
        "gpa": gpa
    })


def logout_user(request):
    logout(request)
    return redirect("login")
