# Generated by Django 3.2.16 on 2023-01-09 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0062_alter_formlogic_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="form",
            name="include_confirmation_page_content_in_pdf",
            field=models.BooleanField(
                default=True,
                help_text="Display the instruction from the confirmation page in the PDF.",
                verbose_name="include confirmation page content in PDF",
            ),
        ),
    ]