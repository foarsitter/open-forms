# Generated by Django 3.2.13 on 2022-06-01 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0025_formvariable_valid prefill configuration"),
        ("submissions", "0053_submission_registration_attempts"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubmissionValueVariable",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "key",
                    models.SlugField(
                        help_text="Key of the variable",
                        max_length=100,
                        verbose_name="key",
                    ),
                ),
                (
                    "value",
                    models.JSONField(
                        blank=True,
                        help_text="The value of the variable",
                        null=True,
                        verbose_name="value",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[
                            ("static", "Static"),
                            ("sensitive_data_cleaner", "Sensitive data cleaner"),
                            ("user_input", "User input"),
                            ("prefill", "Prefill"),
                            ("logic", "Logic"),
                            ("dmn", "DMN"),
                        ],
                        help_text="Where variable value came from",
                        max_length=50,
                        verbose_name="source",
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        blank=True,
                        help_text="If this value contains text, in which language is it?",
                        max_length=50,
                        verbose_name="language",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The date/time at which the value of this variable was created",
                        verbose_name="created at",
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The date/time at which the value of this variable was last set",
                        null=True,
                        verbose_name="modified at",
                    ),
                ),
                (
                    "form_variable",
                    models.ForeignKey(
                        help_text="The form variable to which this value is related",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="forms.formvariable",
                        verbose_name="form variable",
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        help_text="The submission to which this variable value is related",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="submissions.submission",
                        verbose_name="submission",
                    ),
                ),
            ],
            options={
                "verbose_name": "Submission value variable",
                "verbose_name_plural": "Submission values variables",
                "unique_together": {
                    ("submission", "form_variable"),
                    ("submission", "key"),
                },
            },
        ),
    ]
