from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings






def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")   # 🔑 match your HTML field name

        # Check empty fields
        if not username or not password:
            messages.error(request, "Both fields are required.")
            return redirect("signup")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # Auto-login the user
        login(request, user)

        return redirect("dashboard")

    return render(request, "accounts/signup.html")




def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to dashboard after successful login
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, "accounts/login.html", {"error": "Invalid username or password"})
    return render(request, "accounts/login.html")



@login_required(login_url=settings.LOGIN_URL)
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")



def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
