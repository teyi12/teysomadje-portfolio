import logging
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import BadHeaderError, EmailMessage
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import Project


logger = logging.getLogger(__name__)


def home(request):
    projects = Project.objects.filter(featured=True)

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            contact_email = EmailMessage(
                subject="New portfolio contact",
                body=(
                    f"Name: {name}\n"
                    f"Email: {email}\n\n"
                    f"Message:\n{message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[email],
            )

            try:
                contact_email.send(fail_silently=False)
            except (BadHeaderError, SMTPException, OSError):
                logger.exception("Portfolio contact email could not be sent.")
                messages.error(
                    request,
                    "Your message could not be sent. Please try again later.",
                )
            else:
                messages.success(
                    request,
                    "Your message has been sent successfully.",
                )
                return redirect("home")

    else:
        form = ContactForm()

    return render(
        request,
        "portfolio/home.html",
        {
            "form": form,
            "projects": projects,
        },
    )
