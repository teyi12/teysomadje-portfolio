from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=150)

    slug = models.SlugField(
        max_length=160,
        unique=True,
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
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