from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django_countries import countries
from datetime import datetime

# Create your views here.
from .forms import CreateUserForm
from .utils import account_activation_token
from .models import CustomUser
from funds.models.project import Project
from funds.models.donation import Donation


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        user_form = CreateUserForm()

        if request.method == "POST":
            user_form = CreateUserForm(request.POST)
            if user_form.is_valid():

                user = user_form.save(commit=False)
                #
                user.is_active = False
                user.save()

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                current_site = get_current_site(request)
                link = reverse('activate', kwargs={
                    'uidb64': uid, 'token': token})
                activate_url = 'http://' + current_site.domain + link

                email_subject = 'Activate your account'
                email_body = f"hi {user.username}. Please use this link to verify your account {activate_url}"

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semicolon.com',
                    [user.email]
                )
                email.send(fail_silently=False)

                messages.success(request, "Account create. Please check your email for activation")
                return redirect("login")

        context = {"form": user_form}
        return render(request, "accounts/register.html", context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect("egyfund")
    else:
        if request.method == "POST":
            username = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("egyfund")
            else:
                messages.info(request, "Invalid Credentials!")

        context = {}
        return render(request, "accounts/login.html", context)


def logout_user(request):
    logout(request)
    return redirect("login")


def verify(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=user_id)

        if not account_activation_token.check_token(user, token):
            messages.warning(request, 'User already activated')
            return redirect('login')

        user.is_active = True
        user.save()

        messages.success(request, 'Account activated successfully')
        return redirect('login')

    except Exception as ex:
        pass

    return redirect('login')


@login_required
@csrf_protect
def profile(request, user_id):
    # Getting the user hotting that end point
    user = get_object_or_404(CustomUser, id=user_id)
    # Checking if this is the profile of the user requesting the page
    if request.user.id != user_id:
        projects = Project.objects.filter(user=user)
        context = {
            "user": user,
            "projects_count": projects.count,
            "birthday": user.birth_date.strftime("%Y-%m-%d") if user.birth_date else None
        }
        return render(request, "accounts/profile_guest.html", context)

    # We get the data to save
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        birth_date = request.POST.get("birth_date")
        facebook_profile = request.POST.get("facebook_profile")
        country = request.POST.get("country")
        image = None
        if request.FILES:
            image = request.FILES['image']
            user.image = image
        # Checking if data to update is valid
        if not username or not first_name or not last_name or not phone_number:
            messages.error(request, "Username, First name, Last name and Phone can't be empty!")
        else:  # Form is valid
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            # The reason we do that check in because birth_date if available, is of type string.
            # So we convert it to date time else we set it to None
            if not birth_date:
                user.birth_date = None
            else:
                user.birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
            user.facebook_profile = facebook_profile
            user.country = country
            user.image = image
            user.save()
            messages.success(request, "Profile Updated Successfully.")

    # Get method, also this renders the view after a post request
    projects = Project.objects.filter(user=user)
    donations = Donation.objects.filter(user=user)
    user_form = CreateUserForm(instance=user)
    context = {
        "user": user,
        "projects_count": projects.count,
        "donations_count": donations.count,
        "form": user_form,
        "countries": countries,
        "birthday": user.birth_date.strftime("%Y-%m-%d") if user.birth_date else None
    }
    return render(request, "accounts/profile.html", context)


@login_required
def index(request):
    context = {
        "user": request.user
    }
    return render(request, "accounts/index.html", context)


# @login_required(login_url='/myAuth/')
@login_required
def test(request):
    return HttpResponse("test is working!")


@login_required
def user_projects(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    projects = Project.objects.filter(user=user)
    context = {
        "user": user,
        "projects": projects
    }
    return render(request, "accounts/profile_projects.html", context)


@login_required
def forbidden(request):
    return render(request, "accounts/forbidden.html")


@login_required
def user_donations(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.id != request.user.id:
        return redirect("forbidden")
    donations = Donation.objects.filter(user=user)
    context = {
        "user": user,
        "donations": donations
    }
    return render(request, "accounts/profile_donations.html", context)


@login_required
def profile_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.id != request.user.id:
        return redirect("forbidden")
    context = {
        "user": user,
    }
    return render(request, "accounts/profile_delete.html", context)


@login_required
def profile_delete_confirm(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.id != request.user.id:
        return redirect("forbidden")
    # print("Account deleted")
    user = CustomUser.objects.get(id=request.user.id)
    user.delete()
    messages.success(request, "Account has been deleted.")
    return redirect("logout")
