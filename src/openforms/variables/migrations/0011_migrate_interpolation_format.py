# Generated by Django 3.2.18 on 2023-03-28 12:35

import re

from django.db import migrations

MATCH_SINGLE_BRACKETS = r"{([A-z0-9_\.]*)}"
REPL_SINGLE_BRACKETS = r"{{\1}}"


def apply_regex_nested(data, pattern, repl):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = apply_regex_nested(value, pattern, repl)
    elif isinstance(data, list):
        data = [apply_regex_nested(value, pattern, repl) for value in data]
    elif isinstance(data, str):
        return re.sub(pattern, repl, data)
    return data


def forwards(apps, _):
    ServiceFetchConfiguration = apps.get_model("variables", "ServiceFetchConfiguration")

    for config in ServiceFetchConfiguration.objects.all():
        if config.body:
            config.body = apply_regex_nested(
                config.body, MATCH_SINGLE_BRACKETS, REPL_SINGLE_BRACKETS
            )
        if config.headers:
            config.headers = apply_regex_nested(
                config.headers, MATCH_SINGLE_BRACKETS, REPL_SINGLE_BRACKETS
            )
        if config.query_params:
            config.query_params = apply_regex_nested(
                config.query_params, MATCH_SINGLE_BRACKETS, REPL_SINGLE_BRACKETS
            )

        config.save()


class Migration(migrations.Migration):

    dependencies = [
        ("variables", "0010_alter_servicefetchconfiguration_name"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
