# Generated by Django 3.2.18 on 2023-05-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0072_set_preregistration_complete"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="submission",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("registration_status", "success"),
                    ("pre_registration_completed", False),
                    _negated=True,
                ),
                name="registration_status_consistency_check",
            ),
        ),
    ]
