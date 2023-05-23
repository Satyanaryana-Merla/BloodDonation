"""from django.contrib.auth import views as auth_views"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # import this
from django.urls import path
from DonorApp import views

urlpatterns = [
    path("login/", views.login_request, name="login"),
    path("signup/", views.signup, name="signup"),
    path("donor_details/", views.donor_list, name="donor_details"),
    path("donordetails/", views.donordetails, name="donordetails"),
    path('send_email/', views.send_emails, name='send_email'),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("logout/", views.logoutpage, name="logout"),
    path(
        "password_reset/",
        views.password_reset_request,
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password/password_reset_done.html"
        ),  # noqa: E501
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password/password_reset_confirm.html"
        ),  # noqa: E501
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password/password_reset_complete.html"
        ),  # noqa: E501
        name="password_reset_complete",
    ),

    # path("edit_donordetails/", views.edit_donordetails, name="edit_donordetails"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
