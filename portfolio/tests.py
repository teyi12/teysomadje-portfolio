import json
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation

from .models import ContactSubmission, Project


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

    def test_localized_content_uses_translation_and_falls_back_to_english(self):
        project = Project(
            title="English title",
            title_de="Deutscher Titel",
            description="English description",
            description_de="Deutsche Beschreibung",
        )

        with translation.override("de"):
            self.assertEqual(project.localized_title, "Deutscher Titel")
            self.assertEqual(project.localized_description, "Deutsche Beschreibung")

        with translation.override("fr"):
            self.assertEqual(project.localized_title, "English title")
            self.assertEqual(project.localized_description, "English description")

    def test_legacy_hero_project_image_is_detected(self):
        project = Project(
            image_url=(
                "https://example.com/static/portfolio/img/hero/hero-assets.png"
            )
        )

        self.assertTrue(project.uses_legacy_hero_image)


@override_settings(
    BREVO_API_URL="https://api.brevo.test/v3/smtp/email",
    BREVO_API_KEY="test-api-key",
    BREVO_TIMEOUT=10,
    DEFAULT_FROM_EMAIL="verified@example.com",
    CONTACT_EMAIL="owner@example.com",
    CONTACT_RATE_LIMIT=2,
    CONTACT_RATE_WINDOW_SECONDS=3600,
)
class HomeViewTests(TestCase):
    def setUp(self):
        translation.activate("en")
        self.url = "/en/"
        self.featured_project = Project.objects.create(
            title="Featured project",
            title_de="Ausgewähltes Projekt",
            title_fr="Projet présenté",
            slug="featured-project",
            description="Visible on the portfolio.",
            description_de="Im Portfolio sichtbar.",
            description_fr="Visible dans le portfolio.",
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

    def tearDown(self):
        translation.deactivate()

    def test_home_page_loads_successfully(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/home.html")

    def test_home_page_displays_optimized_about_portrait(self):
        response = self.client.get(self.url)

        self.assertContains(
            response,
            "portfolio/img/teyi-portrait.",
        )
        self.assertContains(
            response,
            "Portrait of Teyi Guillaume Lawson-Somadje",
        )
        self.assertContains(response, 'loading="lazy"')

    def test_home_page_uses_responsive_hero_images(self):
        response = self.client.get(self.url)

        self.assertContains(response, "hero-assets-640.")
        self.assertContains(response, "hero-assets-960.")
        self.assertContains(response, "hero-assets-1536.")
        self.assertContains(response, 'fetchpriority="high"')
        self.assertContains(response, 'width="1536"')
        self.assertContains(response, 'height="1024"')

    def test_home_page_contains_canonical_and_social_metadata(self):
        response = self.client.get(
            self.url,
            secure=True,
        )

        self.assertContains(
            response,
            '<link rel="canonical" href="https://testserver/en/">',
            html=True,
        )
        self.assertContains(
            response,
            '<meta property="og:type" content="website">',
            html=True,
        )
        self.assertContains(
            response,
            "https://testserver/static/portfolio/img/brand/social-card.",
        )
        self.assertContains(response, 'property="og:image:width" content="1200"')
        self.assertContains(response, 'rel="icon"')
        self.assertContains(response, 'rel="manifest"')
        self.assertContains(response, '"@type": "Person"')
        self.assertContains(
            response,
            'name="google-site-verification"',
        )
        self.assertContains(
            response,
            "YbInrVqq5hfxF1drNcYUQc8CgyvPghXS7tQhGY5ZHlI",
        )

    def test_robots_txt_allows_crawling_and_links_sitemap(self):
        response = self.client.get(
            reverse("robots_txt"),
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "User-agent: *")
        self.assertContains(
            response,
            "Sitemap: https://testserver/sitemap.xml",
        )

    def test_sitemap_contains_home_page(self):
        response = self.client.get(
            reverse("sitemap"),
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, "<loc>https://testserver/en/</loc>")
        self.assertContains(response, "<loc>https://testserver/de/</loc>")
        self.assertContains(response, "<loc>https://testserver/fr/</loc>")

    def test_language_versions_render_translated_interface_and_content(self):
        german = self.client.get("/de/")
        french = self.client.get("/fr/")

        self.assertContains(german, '<html lang="de">')
        self.assertContains(german, "Ausgewählte Projekte")
        self.assertContains(german, "Ausgewähltes Projekt")
        self.assertContains(french, '<html lang="fr">')
        self.assertContains(french, "Projets à la une")
        self.assertContains(french, "Projet présenté")

    def test_home_page_exposes_language_alternates(self):
        response = self.client.get("/en/", secure=True)

        self.assertContains(
            response,
            '<link rel="alternate" hreflang="de" href="https://testserver/de/">',
            html=True,
        )
        self.assertContains(
            response,
            '<link rel="alternate" hreflang="fr" href="https://testserver/fr/">',
            html=True,
        )

    def test_home_page_displays_only_featured_projects(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.featured_project.title)
        self.assertNotContains(response, self.hidden_project.title)

    def test_external_image_url_is_rendered(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.featured_project.image_url)
        self.assertContains(response, 'loading="lazy"')

    def test_legacy_hero_project_uses_lightweight_thumbnail(self):
        self.featured_project.image_url = (
            "https://example.com/static/portfolio/img/hero/hero-assets.png"
        )
        self.featured_project.save(update_fields=["image_url"])

        response = self.client.get(self.url)

        self.assertContains(response, "hero-assets-640.")
        self.assertNotContains(response, self.featured_project.image_url)

    @patch("portfolio.views.urlopen")
    def test_invalid_contact_form_does_not_call_brevo(self, mocked_urlopen):
        response = self.client.post(
            self.url,
            {
                "name": "",
                "email": "invalid-email",
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        mocked_urlopen.assert_not_called()
        self.assertContains(response, "This field is required.")

    @patch("portfolio.views.urlopen")
    def test_honeypot_submission_fakes_success_without_calling_brevo(
        self,
        mocked_urlopen,
    ):
        response = self.client.post(
            self.url,
            {
                "name": "Spam Bot",
                "email": "bot@example.com",
                "message": "Automated advertisement.",
                "website": "https://spam.example.com",
            },
            follow=True,
        )

        self.assertRedirects(response, self.url)
        mocked_urlopen.assert_not_called()
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertContains(
            response,
            "Your message has been sent successfully.",
        )

    @patch("portfolio.views.urlopen")
    def test_valid_contact_form_calls_brevo_and_redirects(
        self,
        mocked_urlopen,
    ):
        mocked_response = MagicMock()
        mocked_response.status = 201
        mocked_urlopen.return_value.__enter__.return_value = mocked_response

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
        mocked_urlopen.assert_called_once()
        brevo_request = mocked_urlopen.call_args.args[0]
        payload = json.loads(brevo_request.data.decode("utf-8"))

        self.assertEqual(brevo_request.full_url, "https://api.brevo.test/v3/smtp/email")
        self.assertEqual(brevo_request.get_method(), "POST")
        self.assertEqual(brevo_request.headers["Api-key"], "test-api-key")
        self.assertEqual(payload["sender"]["email"], "verified@example.com")
        self.assertEqual(payload["to"], [{"email": "owner@example.com"}])
        self.assertEqual(
            payload["replyTo"],
            {"name": "Test Visitor", "email": "visitor@example.com"},
        )
        self.assertIn("visitor@example.com", payload["textContent"])
        self.assertContains(
            response,
            "Your message has been sent successfully.",
        )

    @patch("portfolio.views.urlopen")
    def test_rate_limit_blocks_third_submission_from_same_ip(
        self,
        mocked_urlopen,
    ):
        mocked_response = MagicMock()
        mocked_response.status = 201
        mocked_urlopen.return_value.__enter__.return_value = mocked_response
        form_data = {
            "name": "Test Visitor",
            "email": "visitor@example.com",
            "message": "Please contact me.",
        }

        for _ in range(2):
            response = self.client.post(
                self.url,
                form_data,
                REMOTE_ADDR="203.0.113.10",
            )
            self.assertEqual(response.status_code, 302)

        response = self.client.post(
            self.url,
            form_data,
            REMOTE_ADDR="203.0.113.10",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mocked_urlopen.call_count, 2)
        self.assertEqual(ContactSubmission.objects.count(), 2)
        self.assertNotIn(
            "203.0.113.10",
            ContactSubmission.objects.first().ip_hash,
        )
        self.assertContains(
            response,
            "Too many messages have been sent. Please try again later.",
        )

    @patch(
        "portfolio.views.urlopen",
        side_effect=URLError("Brevo unavailable"),
    )
    def test_brevo_failure_keeps_form_and_shows_error(
        self,
        mocked_urlopen,
    ):
        response = self.client.post(
            self.url,
            {
                "name": "Test Visitor",
                "email": "visitor@example.com",
                "message": "Please contact me.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Your message could not be sent. Please try again later.",
        )
        mocked_urlopen.assert_called_once()
