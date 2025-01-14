# Generated by Django 3.2.16 on 2022-11-17 16:46
from django.db import migrations

from openforms.formio.utils import iter_components


def make_hide_label_false(apps, _):
    FormDefinition = apps.get_model("forms", "FormDefinition")

    form_definitions = FormDefinition.objects.all()
    form_definitions_to_update = []
    for form_definition in form_definitions:
        updated_form_definition = False
        for comp in iter_components(configuration=form_definition.configuration):
            if comp["type"] != "editgrid" or not comp.get("hideLabel", False):
                continue
            comp["hideLabel"] = False
            updated_form_definition = True

        if updated_form_definition:
            form_definitions_to_update.append(form_definition)

    if form_definitions_to_update:
        FormDefinition.objects.bulk_update(
            form_definitions_to_update, fields=["configuration"]
        )


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0054_merge_20221114_1308"),
    ]

    operations = [
        migrations.RunPython(make_hide_label_false, migrations.RunPython.noop),
    ]
