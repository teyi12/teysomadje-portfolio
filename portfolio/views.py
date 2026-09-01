import hashlib
import hmac
import json
import logging
from datetime import timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils import translation
from django.utils.translation import gettext as _

from .forms import ContactForm
from .models import ContactSubmission, Project


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
        "subject": _("New portfolio contact"),
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


def get_client_ip(request):
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()

    return request.META.get("REMOTE_ADDR", "unknown")


def contact_rate_limit_reached(request):
    limit = settings.CONTACT_RATE_LIMIT
    if limit <= 0:
        return False

    cutoff = timezone.now() - timedelta(
        seconds=settings.CONTACT_RATE_WINDOW_SECONDS
    )
    ContactSubmission.objects.filter(created_at__lt=cutoff).delete()

    client_ip = get_client_ip(request)
    ip_hash = hmac.new(
        str(settings.SECRET_KEY).encode("utf-8"),
        client_ip.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    recent_submissions = ContactSubmission.objects.filter(
        ip_hash=ip_hash,
        created_at__gte=cutoff,
    ).count()

    if recent_submissions >= limit:
        return True

    ContactSubmission.objects.create(ip_hash=ip_hash)
    return False


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {sitemap_url}\n"
    )
    return HttpResponse(content, content_type="text/plain")


def home(request):
    projects = Project.objects.filter(featured=True)

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            if form.cleaned_data["website"]:
                logger.info("Contact form honeypot rejected a submission.")
                messages.success(
                    request,
                    _("Your message has been sent successfully."),
                )
                return redirect("home")

            if contact_rate_limit_reached(request):
                messages.error(
                    request,
                    _(
                        "Too many messages have been sent. "
                        "Please try again later."
                    ),
                )
            else:
                try:
                    send_contact_email(
                        name=form.cleaned_data["name"],
                        email=form.cleaned_data["email"],
                        message=form.cleaned_data["message"],
                    )
                except ContactEmailError:
                    logger.exception(
                        "Portfolio contact email could not be sent."
                    )
                    messages.error(
                        request,
                        _(
                            "Your message could not be sent. "
                            "Please try again later."
                        ),
                    )
                else:
                    messages.success(
                        request,
                        _("Your message has been sent successfully."),
                    )
                    return redirect("home")

    else:
        form = ContactForm()

    language_urls = {}
    for language_code, language_name in settings.LANGUAGES:
        with translation.override(language_code):
            language_urls[language_code] = {
                "name": language_name,
                "url": request.build_absolute_uri(reverse("home")),
            }

    return render(
        request,
        "portfolio/home.html",
        {
            "canonical_url": request.build_absolute_uri(reverse("home")),
            "contact_email": settings.CONTACT_EMAIL,
            "form": form,
            "projects": projects,
            "language_urls": language_urls,
            "seo_description": _(
                "Full Stack Web Developer building modern, scalable web "
                "applications with Python, Django and PostgreSQL."
            ),
            "seo_image_url": request.build_absolute_uri(
                static("portfolio/img/brand/social-card.png")
            ),
            "seo_title": _("Teyi Somadje — Full Stack Web Developer"),
        },
    )
