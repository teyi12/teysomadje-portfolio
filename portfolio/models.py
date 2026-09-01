from django.db import models
from django.utils import translation


class Project(models.Model):
    title = models.CharField(max_length=150)

    title_de = models.CharField(max_length=150, blank=True)

    title_fr = models.CharField(max_length=150, blank=True)

    slug = models.SlugField(
        max_length=160,
        unique=True,
    )

    description = models.TextField()

    description_de = models.TextField(blank=True)

    description_fr = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
    )

    image_url = models.URLField(
        blank=True,
        help_text="External image URL used in production.",
    )

    technologies = models.CharField(
        max_length=250,
        help_text="Example: Django, Bootstrap, PostgreSQL",
    )

    github_url = models.URLField(
        blank=True,
    )

    live_url = models.URLField(
        blank=True,
    )

    featured = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def technology_list(self):
        return [
            technology.strip()
            for technology in self.technologies.split(",")
            if technology.strip()
        ]

    @property
    def localized_title(self):
        language = (translation.get_language() or "en").split("-")[0]
        return getattr(self, f"title_{language}", "") or self.title

    @property
    def localized_description(self):
        language = (translation.get_language() or "en").split("-")[0]
        return getattr(self, f"description_{language}", "") or self.description


class ContactSubmission(models.Model):
    ip_hash = models.CharField(
        max_length=64,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]
