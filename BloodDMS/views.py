from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from BloodDMS.models import (Register, BloodRequest, BloodNotification,)
from datetime import date
from dateutil.relativedelta import relativedelta

def font_page(request):
    return render(request, "font_page.html")

@never_cache
def home(request):
    return render(request, "home.html")


# Register view
def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        whatsapp_number = request.POST.get("whatsapp_number")
        other_number = request.POST.get("other_number")
        address = request.POST.get("address")

        blood_group = request.POST.get("blood_group")
        last_donation_date = request.POST.get("last_donation_date")

        # -------------------------
        # Check password
        # -------------------------
        if password != confirm_password:
            return render(
                request,
                "register_user.html",
                {"error": "Passwords do not match."},
            )

        # -------------------------
        # Check username
        # -------------------------
        if Register.objects.filter(username=username).exists():
            return render(
                request,
                "register_user.html",
                {"error": "Username already exists."},
            )

        # -------------------------
        # Create user
        # -------------------------
        user = Register(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            whatsapp_number=whatsapp_number,
            other_number=other_number,
            address=address,
            blood_group=blood_group,
            last_donation_date=last_donation_date or None,
        )

        # Hash password
        user.set_password(password)
        user.save()

        # -------------------------
        # Registration successful
        # Go to login page
        # -------------------------
        return redirect("login")

    return render(request, "register_user.html")


# Login view
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check whether username exists
        if not Register.objects.filter(username=username).exists():
            return render(
                request,
                "login.html",
                {
                    "error": "No account found with this username.",
                    "no_account": True,
                },
            )

        # Authenticate username and password
        user = authenticate(request, username=username, password=password)


        # Wrong password
        if user is None:
            return render(
                request,
                "login.html",
                {"error": "Incorrect password. Please try again."},
            )

        # Login successful
        auth_login(request, user)
        return redirect("home")

    return render(request, "login.html")


def donor_registration(request):
    if request.method == "POST":
        # Get form data
        is_donor = request.POST.get("is_donor")
        blood_group = request.POST.get("blood_group")
        age = request.POST.get("age")
        weight = request.POST.get("weight")
        last_donation_date = request.POST.get("last_donation_date")
        university_batch = request.POST.get("university_batch")

        # Update logged-in user's information
        user = request.user

        user.is_donor = True if is_donor == "yes" else False
        user.blood_group = blood_group
        user.age = age
        user.weight = weight
        user.last_donation_date = last_donation_date or None
        user.university_batch = university_batch

        # Save to database
        user.save()

        # After successful registration
        return redirect("home")

    return render(request, "donor_registration.html")


def blood_search(request):
    blood_group = request.GET.get("blood_group", "")

    # Only show users who are registered as donors
    donors = Register.objects.filter(is_donor=True)

    # Filter by blood group if selected
    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    context = {
        "donors": donors,
        "blood_group": blood_group,
    }

    return render(request, "blood_search.html", context)


def donor_profile(request):
    user = request.user

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "profile":
            user.first_name = request.POST.get("first_name", "").strip()
            user.last_name = request.POST.get("last_name", "").strip()
            user.email = request.POST.get("email", "").strip()
            user.whatsapp_number = request.POST.get("whatsapp_number", "").strip()
            user.other_number = request.POST.get("other_number", "").strip()
            user.address = request.POST.get("address", "").strip()
            user.blood_group = request.POST.get("blood_group")
            user.age = request.POST.get("age") or None
            user.weight = request.POST.get("weight") or None
            user.university_batch = request.POST.get("university_batch", "").strip()
            user.last_donation_date = request.POST.get("last_donation_date") or None
            user.is_donor = request.POST.get("is_donor") == "yes"
            user.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("donor_profile")

        elif form_type == "password":
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            # Check current password
            if not user.check_password(current_password):
                messages.error(request, "Your current password is incorrect.")
                return redirect("donor_profile")

            # Check new password
            if len(new_password) < 8:
                messages.error(request, "New password must contain at least 8 characters.")
                return redirect("donor_profile")

            # Check confirmation
            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect("donor_profile")

            # Change password
            user.set_password(new_password)
            user.save()

            # Keep user logged in
            update_session_auth_hash(request, user)

            messages.success(request, "Your password has been changed successfully.")
            return redirect("donor_profile")

    return render(request, "donor_profile.html", {"user": user})


@login_required
def request_blood(request):

    if request.method == "POST":

        patient_problem = request.POST.get("patient_problem")
        blood_amount = request.POST.get("blood_amount")
        blood_group = request.POST.get("blood_group")
        required_date = request.POST.get("required_date")
        required_time = request.POST.get("required_time")
        phone_number = request.POST.get("phone_number")
        hospital_name = request.POST.get("hospital_name")

        # ==========================================
        # CREATE BLOOD REQUEST
        # ==========================================

        blood_request = BloodRequest.objects.create(
            patient_problem=patient_problem,
            blood_amount=blood_amount,
            blood_group=blood_group,
            required_date=required_date,
            required_time=required_time,
            phone_number=phone_number,
            hospital_name=hospital_name,
            requested_by=request.user,
        )

        # ==========================================
        # NOTIFICATION MESSAGE
        # ==========================================

        message = (
            f"Blood needed: {blood_group}\n"
            f"Patient problem: {patient_problem}\n"
            f"Amount: {blood_amount} bag(s)\n"
            f"Hospital: {hospital_name}\n"
            f"Date: {required_date}\n"
            f"Time: {required_time}\n"
            f"Contact: {phone_number}"
        )

        # ==========================================
        # 1. ADMIN GETS ALL BLOOD GROUP REQUESTS
        # ==========================================

        admins = Register.objects.filter(
            is_staff=True
        )

        for admin in admins:

            BloodNotification.objects.create(
                donor=admin,
                blood_request=blood_request,
                message=message
            )

        # ==========================================
        # 2. FIND ONLY SAME BLOOD GROUP DONORS
        # ==========================================

        today = date.today()

        three_months_ago = (
            today - relativedelta(months=3)
        )

        donors = Register.objects.filter(
            is_donor=True,
            blood_group=blood_group
        ).exclude(
            is_staff=True
        )

        # ==========================================
        # 3. CHECK DONOR ELIGIBILITY
        # ==========================================

        for donor in donors:

            # Never donated before
            if donor.last_donation_date is None:

                eligible = True

            # Last donation was at least 3 months ago
            elif donor.last_donation_date <= three_months_ago:

                eligible = True

            # Donated within the last 3 months
            else:

                eligible = False

            # ======================================
            # SEND NOTIFICATION
            # ======================================

            if eligible:

                BloodNotification.objects.create(
                    donor=donor,
                    blood_request=blood_request,
                    message=message
                )

        messages.success(
            request,
            "Blood request submitted successfully. "
            "Matching donors and admin have been notified."
        )

        return redirect("notifications")

    return render(
        request,
        "request_blood.html"
    )

@login_required
def notifications(request):

    notifications = BloodNotification.objects.filter(
        donor=request.user
    ).select_related(
        "blood_request",
        "blood_request__requested_by"
    ).order_by(
        "-created_at"
    )


    # Mark notifications as read
    BloodNotification.objects.filter(
        donor=request.user,
        is_read=False
    ).update(
        is_read=True
    )


    return render(
        request,
        "notifications.html",
        {
            "notifications": notifications
        }
    )

def donation_benefits(request):
    return render(request, "donation_benefits.html")

# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required
def admin_dashboard(request):

    # -----------------------------------------------------
    # ONLY ADMIN CAN ACCESS
    # -----------------------------------------------------

    if not request.user.is_superuser:
        messages.error(
            request,
            "You do not have permission to access the Admin Dashboard."
        )

        return redirect("home")


    # -----------------------------------------------------
    # HANDLE ROLE CHANGE
    # -----------------------------------------------------

    if request.method == "POST":

        # Get selected user ID
        user_id = request.POST.get("user_id")

        # Get selected role
        role = request.POST.get("role")


        # Find user
        user = get_object_or_404(
            Register,
            id=user_id
        )


        # -------------------------------------------------
        # NORMAL USER
        # -------------------------------------------------

        if role == "user":

            user.is_staff = False
            user.is_superuser = False

            user.save()

            messages.success(
                request,
                f"{user.username} is now a normal User."
            )


        # -------------------------------------------------
        # MODERATOR
        # -------------------------------------------------

        elif role == "moderator":

            user.is_staff = True
            user.is_superuser = False

            user.save()

            messages.success(
                request,
                f"{user.username} has been appointed as Moderator."
            )


        # -------------------------------------------------
        # ADMIN
        # -------------------------------------------------

        elif role == "admin":

            user.is_staff = True
            user.is_superuser = True

            user.save()

            messages.success(
                request,
                f"{user.username} has been appointed as Admin."
            )


        # -------------------------------------------------
        # INVALID ROLE
        # -------------------------------------------------

        else:

            messages.error(
                request,
                "Invalid role selected."
            )


        # After saving, reload dashboard
        return redirect("admin_dashboard")


    # =====================================================
    # GET REQUEST
    # =====================================================

    # Get ALL registered members
    users = Register.objects.all().order_by("username")


    # =====================================================
    # CONTEXT
    # =====================================================

    context = {
        "users": users,
    }


    # =====================================================
    # SHOW ADMIN DASHBOARD
    # =====================================================

    return render(
        request,
        "admin_dashboard.html",
        context
    )