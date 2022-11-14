# Generated by Django 3.2.16 on 2022-11-10 10:05

from django.db import migrations
from django.urls import resolve

from furl import furl

from ..constants import LogicActionTypes


def replace_form_step_urls_with_uuids(apps, schema_editor):
    FormLogic = apps.get_model("forms", "FormLogic")

    rules = FormLogic.objects.all()

    updated_rules = []
    for rule in rules:
        rule_modified = False
        for action in rule.actions:
            action_type = action.get("action", {}).get("type")
            if action_type and action_type == LogicActionTypes.step_not_applicable:
                form_step_url = action["form_step"]
                form_step_uuid = resolve(furl(form_step_url).pathstr).kwargs["uuid"]

                action["form_step_uuid"] = form_step_uuid
                rule_modified = True

        if rule_modified:
            updated_rules.append(rule)

    FormLogic.objects.bulk_update(updated_rules, fields=["actions"])


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0050_alter_formvariable_key"),
    ]

    operations = [
        migrations.RunPython(
            replace_form_step_urls_with_uuids, migrations.RunPython.noop
        ),
    ]
