# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0003_auto_20150216_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='songversion',
            name='chord_versions',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]
