# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_instruments(apps, schema_editor):
    InstrumentModel = apps.get_model('song', 'InstrumentModel')
    db_alias = schema_editor.connection.alias
    InstrumentModel.objects.using(db_alias).bulk_create([
        InstrumentModel(name='Lindsay', definition='guitar'),
        InstrumentModel(name='Edi', definition='ukelele'),
        InstrumentModel(name='Mimi', definition='loog'),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.operations.RunPython(create_instruments)
    ]
