# Generated by Django 2.2.24 on 2021-09-08 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0003_auto_20210907_0956"),
    ]

    operations = [
        migrations.AddField(
            model_name="globalconfiguration",
            name="cancel_appointment_page",
            field=models.URLField(
                blank=True,
                help_text="URL to the page where the user can cancel an appointment.",
                verbose_name="cancel appointment page",
            ),
        ),
    ]