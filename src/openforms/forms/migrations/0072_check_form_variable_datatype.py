# Generated by Django 3.2.18 on 2023-03-06 07:50

from django.db import migrations

from openforms.formio.utils import iter_components
from openforms.variables.constants import FormVariableDataTypes


def check_form_variable_datatype(apps, schema_editor):
    FormVariable = apps.get_model("forms", "FormVariable")
    form_variables = FormVariable.objects.filter(
        data_type=FormVariableDataTypes.datetime
    ).exclude(form_definition=None)

    form_variables_to_update = []
    for form_var in form_variables:
        updated_form_var = False

        form_def = form_var.form_definition
        for comp in iter_components(configuration=form_def.configuration):
            if comp["key"] == form_var.key and comp["type"] == "date":
                form_var.data_type = FormVariableDataTypes.date
                updated_form_var = True

        if updated_form_var:
            form_variables_to_update.append(form_var)

    if form_variables_to_update:
        FormVariable.objects.bulk_update(form_variables_to_update, fields=["data_type"])


class Migration(migrations.Migration):
    dependencies = [("forms", "0071_merge_20230213_1106")]
    operations = [
        migrations.RunPython(check_form_variable_datatype, migrations.RunPython.noop)
    ]
