from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from accounts.models import ConcessionData
from .concession_form import ConcessionDataForm
import json

User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")   # 👈 new field from dropdown

        # Validation
        if not username or not password1 or not password2 or not role:
            messages.error(request, "All fields are required.")
            return redirect("signup")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password1,
            role=role   # 👈 save selected role
        )

        # Auto-login user
        login(request, user)
        messages.success(request, "Account created successfully!")

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
    # check if an active one exists
    active_pass_exists = ConcessionData.objects.filter(
        user_id=request.user.id, is_active=True
    ).exists()

    return render(
        request,
        "accounts/dashboard.html",
        {
            "active_pass_exists": active_pass_exists,  # ✅ now available in templates
        },
    )



def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def apply_concession(request):
    """
    View to display and handle the Concession form.
    Saves submitted data to the existing concession_data table.
    Prevents duplicate active passes for the same user.
    """
    if request.method == 'POST':
        form = ConcessionDataForm(request.POST)
        
        if form.is_valid():
            # ✅ Check if user already has an active pass
            already_active = ConcessionData.objects.filter(
                user_id=request.user.id,
                is_active=1
            ).exists()

            if already_active:
                # Set the session flag and redirect
                request.session['active_pass_exists'] = True
                messages.error(request, "You already have an active pass. You cannot apply again until it expires.")
                
                return redirect('dashboard')

            # ✅ Otherwise, save concession
            obj = form.save(commit=False)
            obj.user_id = request.user.id  # set user_id
            obj.is_active = 1              # mark new pass as active
            obj.status = "Pending"         # default status
            obj.save()

            messages.success(request, "Your concession application has been submitted successfully.")
            return redirect(request,'dashboard')
        else:
            print("Form errors:", form.errors)
    else:
        form = ConcessionDataForm()

    context = {
        'form': form,
        'concessions_taken': 0
    }
    return render(request, "concession_form.html", context)

def epass_view(request, id):
    # Get data from DB
    epass = get_object_or_404(ConcessionData, id=id)

    # Pass it to template
    return render(request, 'epass.html', {'epass': epass})

def epass_view(request, id):
    epass = ConcessionData.objects.get(id=id)
    return render(request, "epass.html", {"epass": epass})

def getActivePass(request):

    User = get_user_model()
    u = User.objects.get(id=request.user.id)
    

    # Fetch the user’s active pass (if exists)
    user_pass = ConcessionData.objects.filter(user_id=request.user.id, is_active=True).first()
    print("sp--")
    print("Active Pass:", user_pass)          # prints <ConcessionData: sailee baliram pawar>
    print("Name:", user_pass.s_name if user_pass else None)
    print("Department:", user_pass.department if user_pass else None)


    # epass = ConcessionData.objects.get(id=id)
    return render(request, "epass.html", {"epass": user_pass})

    return render(request, "dashboard.html", {
        "user_epass": user_pass
    })
