from django.urls import path
from .views import (
    home, register, login_user, dashboard,
    logout_user, profile, grades_dashboard,
    courses, gpa_dashboard
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("profile/", profile, name="profile"),
    path("grades/", grades_dashboard, name="grades"),
    path("courses/", courses, name="courses"),
    path("gpa/", gpa_dashboard, name="gpa"),     # ✅ GPA route added
    path("logout/", logout_user, name="logout"),
]
