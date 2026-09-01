from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0003_contactsubmission"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="description_de",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="project",
            name="description_fr",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="project",
            name="title_de",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="project",
            name="title_fr",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
