from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Project


class ProjectModelTests(TestCase):
    def test_technology_list_strips_whitespace_and_empty_values(self):
        project = Project(
            title="Test project",
            technologies="Django, Bootstrap, , PostgreSQL ",
        )

        self.assertEqual(
            project.technology_list(),
            ["Django", "Bootstrap", "PostgreSQL"],
        )


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="portfolio@example.com",
    CONTACT_EMAIL="owner@example.com",
)
class HomeViewTests(TestCase):
    def setUp(self):
        self.url = reverse("home")
        self.featured_project = Project.objects.create(
            title="Featured project",
            slug="featured-project",
            description="Visible on the portfolio.",
            technologies="Django, PostgreSQL",
            image_url="https://example.com/project.webp",
            featured=True,
        )
        self.hidden_project = Project.objects.create(
            title="Hidden project",
            slug="hidden-project",
            description="Not visible on the portfolio.",
            technologies="Python",
            featured=False,
        )

    def test_home_page_loads_successfully(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/home.html")

    def test_home_page_displays_only_featured_projects(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.featured_project.title)
        self.assertNotContains(response, self.hidden_project.title)

    def test_external_image_url_is_rendered(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.featured_project.image_url)
        self.assertContains(response, 'loading="lazy"')

    def test_invalid_contact_form_does_not_send_email(self):
        response = self.client.post(
            self.url,
            {
                "name": "",
                "email": "invalid-email",
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, "This field is required.")

    def test_valid_contact_form_sends_email_and_redirects(self):
        response = self.client.post(
            self.url,
            {
                "name": "Test Visitor",
                "email": "visitor@example.com",
                "message": "I would like to discuss a Django project.",
            },
            follow=True,
        )

        self.assertRedirects(response, self.url)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Portfolio contact from Test Visitor",
        )
        self.assertIn("visitor@example.com", mail.outbox[0].body)
        self.assertContains(
            response,
            "Your message has been sent successfully.",
        )
