# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0004_songversion_chord_versions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ('title',)},
        ),
    ]
