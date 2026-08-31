from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="image_url",
            field=models.URLField(
                blank=True,
                help_text="External image URL used in production.",
            ),
        ),
    ]
