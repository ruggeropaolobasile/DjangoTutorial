from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    if hasattr(request, "_messages"):
        messages.success(request, f"Welcome back, {user.username}!")


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    if hasattr(request, "_messages"):
        messages.info(request, "You have successfully signed out.")
