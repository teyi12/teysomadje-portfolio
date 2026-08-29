from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "featured",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "featured",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
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