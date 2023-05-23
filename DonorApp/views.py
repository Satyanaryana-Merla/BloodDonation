"""Importing modules"""

from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from DonorApp.forms import CustomUserForm, BloodDonorDetails
from DonorApp.tokens import account_activation_token
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User, Group
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from DonorApp.models import BloodDonorDetailsmodel
from django.contrib.auth.decorators import login_required

# from django.core.mail import send_mail
# from django.conf import settings

# from django.contrib.auth.models import User


# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm


# def home(request):
#     """Home function"""
#     return render(request, "home.html")


def signup(request):
    """regidter"""
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            
            # donorgroup = Group.objects.get(name='user')
            # donorgroup.user_set.add(user)
            user.save()
            # role = form.cleaned_data['role']
            # user.groups.add(Group.objects.get(name=role))
            activateemail(request, user, form.cleaned_data.get("email"))
            return redirect("login")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = CustomUserForm()

    return render(
        request=request, template_name="register.html", context={"form": form}
    )


def activateemail(request, user, to_email):
    """activate email"""
    mail_subject = "Activate your user account."
    message = render_to_string(
        "template_activate_account.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            f"Dear {user}, please go to you email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder.",  # noqa: E501
        )  # noqa: E501
    else:
        messages.error(
            request,
            f"Problem sending confirmation email to {to_email}, check if you typed it correctly.",  # noqa: E501
        )  # noqa: E501


def activate(request, uidb64, token):
    """activate function"""
    User = get_user_model()  # noqa: F821
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."  # noqa: E501
        )
    else:
        return HttpResponse("Activation link is invalid!")


def login_request(request):
    """login_request"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(donor_list)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form}
    )


def logoutpage(request):
    """logoutpage"""
    logout(request)
    return redirect("login")


def donordetails(request):
    """regidter"""
    if request.method == "POST":
        form = BloodDonorDetails(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponse("Your data saved sucessfully")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = BloodDonorDetails()

    return render(
        request=request, template_name="donordetails.html",
        context={"form": form}
    )


# @login_required
# def edit_donordetails(request):
#     """edit_donordetails"""
#     profile = request.user.BloodDonorDetails
#     if request.method == 'POST':
#         form = BloodDonorDetails(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect(edit_donordetails)
#     else:
#         form = BloodDonorDetails(instance=profile)
#     return render(request, 'donordetails.html', {'form': form})


def password_reset_request(request):
    """Password reset"""
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http'
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "AWS_verified_email_address",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    messages.success(
                        request,
                        "A message with reset password instructions has been sent to your inbox.",  # noqa: E501
                    )  # noqa: E501
                    return redirect("login")
            messages.error(request, "An invalid email has been entered.")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )


def donor_list(request):
    donors = BloodDonorDetailsmodel.objects.all()
    if request.method == 'POST':
        selected_donors = request.POST.getlist('selected_donors')
        donors = BloodDonorDetailsmodel.objects.filter(id__in=selected_donors)
        
        for donor in donors:
            subject = 'Blood donation campaign'
            message = f'Hello {donor.name}, we are organizing a blood donation campaign next week. We would like to invite you to participate.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [donor.email]
            send_mail(subject, message, from_email, recipient_list)

        return redirect(send_emails(request))
    else:
        donors = BloodDonorDetailsmodel.objects.all()
        return render(request, 'blood_donor_list.html', {'donors': donors})


def send_emails(request):
    if request.method == 'POST':
        selected_donors = request.POST.getlist('selected_donors')
        donors = BloodDonorDetailsmodel.objects.filter(id__in=selected_donors)

        # Create a list to store the email recipients
        recipient_list = []

        for donor in donors:
            subject = 'Blood donation campaign'
            message = f'Hello {donor.fullname}, we are organizing a blood donation campaign next week. We would like to invite you to participate.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list.append(donor.email)

        # Send email to all selected donors at once
        send_mail(subject, message, from_email, recipient_list)

        return render(request, 'email_sent.html')
    else:
        donors = BloodDonorDetailsmodel.objects.all()
        return render(request, 'donor_list.html', {'donors': donors})



# @login_required
# @login_required
# def send_email(request):
#     if request.method == 'POST':
#         selected_donors = request.POST.getlist('selected_donors')
#         recipients = [donor.email for donor in BloodDonorDetailsmodel.objects.filter(pk__in=selected_donors)]
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#         send_mail(subject, message, 'your_email@example.com', recipients)
#         return render(request, 'email_sent.html')
#     else:
#         donors = BloodDonorDetailsmodel.objects.all()
#         return render(request, 'blood_donor_list.html', {'donors': donors}) 