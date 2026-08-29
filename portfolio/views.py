from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import Project


def home(request):
    projects = Project.objects.filter(featured=True)

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(
                subject=f"Portfolio contact from {name}",
                message=(
                    f"Name: {name}\n"
                    f"Email: {email}\n\n"
                    f"Message:\n{message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            messages.success(
                request,
                "Your message has been sent successfully."
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