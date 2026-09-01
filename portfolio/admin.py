from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_demo",
        "featured",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "featured",
        "is_demo",
        "created_at",
    )

    search_fields = (
        "title",
        "title_de",
        "title_fr",
        "description",
        "description_de",
        "description_fr",
        "technologies",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
