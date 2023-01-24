# Generated by Django 3.2.16 on 2023-01-23 11:52

from django.db import migrations
from glom import assign

from openforms.formio.utils import iter_components


def add_options_source(apps, schema_editor):
    FormDefinition = apps.get_model("forms", "FormDefinition")

    form_definitions = FormDefinition.objects.all()

    form_definitions_to_update = []
    for form_definition in form_definitions:
        updated_form_definition = False

        for comp in iter_components(configuration=form_definition.configuration):
            if comp["type"] in ["radio", "selectboxes"]:
                comp["dataSrc"] = "manual"
                updated_form_definition = True
            elif comp["type"] == "select":
                assign(comp, "data.dataSrc", "manual", missing=dict)
                updated_form_definition = True

        if updated_form_definition:
            form_definitions_to_update.append(form_definition)

    if form_definitions_to_update:
        FormDefinition.objects.bulk_update(
            form_definitions_to_update, fields=["configuration"]
        )


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0066_merge_20230119_1618"),
    ]

    operations = [migrations.RunPython(add_options_source, migrations.RunPython.noop)]
