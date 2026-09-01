from django.db import migrations, models


def create_taskflow_demo(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.get_or_create(
        slug="taskflow-pro",
        defaults={
            "title": "TaskFlow Pro",
            "title_de": "TaskFlow Pro",
            "title_fr": "TaskFlow Pro",
            "description": (
                "A collaborative SaaS dashboard for planning projects, "
                "assigning tasks and tracking team progress. Demo project "
                "currently in development."
            ),
            "description_de": (
                "Ein kollaboratives SaaS-Dashboard für Projektplanung, "
                "Aufgabenzuweisung und Fortschrittsverfolgung. "
                "Demoprojekt in Entwicklung."
            ),
            "description_fr": (
                "Un tableau de bord SaaS collaboratif pour planifier les "
                "projets, attribuer les tâches et suivre l’avancement des "
                "équipes. Projet de démonstration en cours de développement."
            ),
            "static_image": "portfolio/img/projects/taskflow-pro.svg",
            "technologies": "Django, PostgreSQL, Bootstrap, JavaScript",
            "featured": True,
            "is_demo": True,
        },
    )


def remove_taskflow_demo(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.filter(slug="taskflow-pro", is_demo=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0004_project_translations"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="static_image",
            field=models.CharField(
                blank=True,
                help_text=(
                    "Static image path, for example "
                    "portfolio/img/projects/project.svg"
                ),
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="is_demo",
            field=models.BooleanField(
                default=False,
                help_text="Marks a concept or demonstration project.",
            ),
        ),
        migrations.RunPython(
            create_taskflow_demo,
            remove_taskflow_demo,
        ),
    ]
