from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError


# Create your views here.
from .forms import CreateUserForm
from .utils import account_activation_token
from .models import CustomUser


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        user_form = CreateUserForm()

        if request.method == "POST":
            user_form = CreateUserForm(request.POST)
            if user_form.is_valid():

                user = user_form.save(commit=False)
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
def profile(request):
    context = {
        "user": request.user,
        "projects": " ",
        "donations": " "
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
