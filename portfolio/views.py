import json
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import Project


logger = logging.getLogger(__name__)


class ContactEmailError(Exception):
    """Raised when a contact message cannot be delivered."""


def send_contact_email(*, name, email, message):
    if not settings.BREVO_API_KEY:
        raise ContactEmailError("BREVO_API_KEY is not configured.")

    payload = {
        "sender": {
            "name": "Teyi Somadje Portfolio",
            "email": settings.DEFAULT_FROM_EMAIL,
        },
        "to": [{"email": settings.CONTACT_EMAIL}],
        "replyTo": {"name": name, "email": email},
        "subject": "New portfolio contact",
        "textContent": (
            f"Name: {name}\n"
            f"Email: {email}\n\n"
            f"Message:\n{message}"
        ),
    }
    brevo_request = Request(
        settings.BREVO_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(
            brevo_request,
            timeout=settings.BREVO_TIMEOUT,
        ) as response:
            if not 200 <= response.status < 300:
                raise ContactEmailError(
                    f"Brevo returned HTTP {response.status}."
                )
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise ContactEmailError("Brevo request failed.") from exc


def home(request):
    projects = Project.objects.filter(featured=True)

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            if form.cleaned_data["website"]:
                logger.info("Contact form honeypot rejected a submission.")
                messages.success(
                    request,
                    "Your message has been sent successfully.",
                )
                return redirect("home")

            try:
                send_contact_email(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                    message=form.cleaned_data["message"],
                )
            except ContactEmailError:
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
