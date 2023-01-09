# Generated by Django 3.2.16 on 2022-12-22 11:31

from django.db import migrations
from django.utils.translation import gettext

from openforms.utils.json_logic import generate_rule_description


def generate_natural_language_descriptions(apps, _):
    FormLogic = apps.get_model("forms", "FormLogic")
    for form_logic in FormLogic.objects.filter(description="").iterator():
        description = generate_rule_description(form_logic.json_logic_trigger)
        form_logic.description = gettext("When {trigger}").format(trigger=description)[
            :100
        ]
        form_logic.save(update_fields=["description"])


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0060_formlogic_description"),
    ]

    operations = [
        migrations.RunPython(
            generate_natural_language_descriptions, migrations.RunPython.noop
        ),
    ]