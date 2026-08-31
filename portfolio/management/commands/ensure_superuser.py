import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the initial superuser from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not all((username, email, password)):
            self.stdout.write(
                "Superuser environment variables are incomplete; skipping."
            )
            return

        user_model = get_user_model()

        if user_model.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING("Superuser already exists; skipping.")
            )
            return

        user_model.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
