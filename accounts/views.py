from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from accounts.models import ConcessionData
from .concession_form import ConcessionDataForm
import json, re

User = get_user_model()
def home(request):
    return render(request, "accounts/home.html")

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
        
        # ✅ Password Strength Validation
        if len(password1) < 10:
            messages.error(request, "Password must be at least 10 characters long.")
            return redirect("signup")

        if not re.search(r"[A-Z]", password1):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect("signup")

        if not re.search(r"[a-z]", password1):
            messages.error(request, "Password must contain at least one lowercase letter.")
            return redirect("signup")

        if not re.search(r"[0-9]", password1):
            messages.error(request, "Password must contain at least one digit.")
            return redirect("signup")

        if not re.search(r"[@$!%*?&#]", password1):
            messages.error(request, "Password must contain at least one special character (@, $, !, %, *, ?, &, #).")
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
        role = request.POST.get("role")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 🔎 Check if role exists in DB
            try:
                db_user = User.objects.get(username=username)
                if db_user and role.lower() != db_user.role :
                    messages.error(request, "Your account does not have a role assigned. Contact admin.")
                    return render(request, "accounts/login.html", {"error": "Your account does not have a role assigned. Contact admin."})
            
            except User.DoesNotExist:
                # messages.error(request, "User not found.")
                # return redirect("login")
                return render(request, "accounts/login.html", {"error": "User not found."})

            # ✅ Login the user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, "accounts/login.html", {"error": "Invalid username or password"})
    return render(request, "accounts/login.html")



@login_required(login_url=settings.LOGIN_URL)
def dashboard_view(request):
    # check if an active one exists

    if request.user.role == "admin":
        pending_concessions = ConcessionData.objects.filter(is_active=2)  # status=2 => Pending
    else:
        active_pass_exists = ConcessionData.objects.filter(
            user_id=request.user.id, is_active=True
        ).exists()
        pending_concessions = None

    # Fetch total concessions taken by the logged-in user
    concessions_count = 0
    concessions_list = []
    if request.user.is_authenticated:
        user_concessions = ConcessionData.objects.filter(user_id=request.user.id)
        concessions_count = user_concessions.count()
        concessions_list = user_concessions

    if request.user.role == "admin":
        return render(
            request,
            "accounts/dashboard.html",
            {
                "pending_concessions": pending_concessions
            },
        )
    else:
        return render(
            request,
            "accounts/dashboard.html",
            {
                "active_pass_exists": active_pass_exists,
                "concessions_taken": concessions_count,
                "concessions_list": concessions_list,
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
                request.session['active_pass_exists'] = True
                messages.error(request, "You already have an active pass. You cannot apply again until it expires.")
                return redirect('dashboard')

            obj = form.save(commit=False)
            obj.user_id = request.user.id
            obj.is_active = 2
            obj.status = "Pending"
            obj.save()

            # ✅ Send confirmation email
            from django.core.mail import send_mail
            from django.conf import settings

            subject = "Concession Application Submitted"
            message = (
                f"Dear {obj.s_name},\n\n"
                f"Your concession application has been submitted successfully.\n"
                f"Duration: {obj.duration} month(s)\n"
                f"Status: {obj.status}\n\n"
                "Thank you for applying."
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [obj.email_id], fail_silently=True)

            messages.success(request, "Your concession application has been submitted successfully and a confirmation email has been sent.")
            return redirect('dashboard')
        else:
            print("Form errors:", form.errors)
    else:
        form = ConcessionDataForm()

    # ✅ Fetch concessions taken
    concessions_count = 0
    if request.user.is_authenticated:
        concessions_count = ConcessionData.objects.filter(user_id=request.user.id).count()

    context = {
        'form': form,
        'concessions_taken': concessions_count
    }
    return render(request, "concession_form.html", context)

def concession_form(request):
    # Get data from DB
    # epass = get_object_or_404(ConcessionData, id=id)

    # Pass it to template
    return render(request, 'concession_form.html')

def epass_view(request, id):
    epass = ConcessionData.objects.get(id=id)
    return render(request, "epass.html", {"epass": epass})

def getActivePass(request):

    User = get_user_model()
    u = User.objects.get(id=request.user.id)
    

    # Fetch the user’s active pass (if exists)
    user_pass = ConcessionData.objects.filter(user_id=request.user.id, is_active=1).first()
    
    print("Active Pass:", user_pass)          # prints <ConcessionData: sailee baliram pawar>
    print("Name:", user_pass.s_name if user_pass else None)
    print("Department:", user_pass.department if user_pass else None)


    # epass = ConcessionData.objects.get(id=id)
    return render(request, "epass.html", {"epass": user_pass})

    return render(request, "dashboard.html", {
        "user_epass": user_pass
    })


#### concession approve/reject part ###
@login_required
def approve_concession(request, pk):
    concession = get_object_or_404(ConcessionData, id=pk, is_active=2)
    concession.is_active = 1  # Approved
    concession.status = "Approved"
    concession.save()
    messages.success(request, "Concession approved successfully ✅")
    return redirect("dashboard")
    # return HttpResponseRedirect(reverse("dashboard") + "?tab=verify")


@login_required
def reject_concession(request, pk):
    concession = get_object_or_404(ConcessionData, id=pk, is_active=2)
    concession.is_active = 0  # Rejected
    concession.status = "Rejected"
    concession.save()
    messages.error(request, "Concession rejected ❌")
    return redirect("dashboard")