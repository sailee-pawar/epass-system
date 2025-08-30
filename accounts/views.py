from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from accounts.models import ConcessionData
from .concession_form import ConcessionDataForm
import json

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


def apply_concession(request):
    """
    View to display and handle the Concession form.
    Saves submitted data to the existing concession_data table.
    """
    print("POST data:", request.POST)
    
    if request.method == 'POST':
        form = ConcessionDataForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            # Optionally associate with logged-in user
            # obj.user_id = request.user.id if hasattr(request.user, 'id') else None
            obj.save()
            return redirect('dashboard')  # reload page after submission
        else:
            print("Form errors:", form.errors)
    else:
        print("in here")
        form = ConcessionDataForm()

    # Count total concessions submitted by the user (optional)
    # concessions_taken = ConcessionData.objects.filter(user_id=request.user.id).count() if hasattr(request.user, 'id') else 0

    context = {
        'form': form,
        'concessions_taken': 0
    }

def epass_view(request, id):
    # Get data from DB
    epass = get_object_or_404(ConcessionData, id=id)

    # Pass it to template
    return render(request, 'epass.html', {'epass': epass})

def epass_view(request, id):
    epass = ConcessionData.objects.get(id=id)
    return render(request, "epass.html", {"epass": epass})

def getActivePass(request):
    # Fetch the user’s active pass (if exists)
    user_pass = ConcessionData.objects.filter(user=request.user, is_active=True).first()

    return render(request, "dashboard.html", {
        "user_epass": user_pass
    })
