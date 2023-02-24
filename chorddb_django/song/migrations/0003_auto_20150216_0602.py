# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0002_basic_instruments'),
    ]

    operations = [
        migrations.AddField(
            model_name='songversion',
            name='capo',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='songversion',
            name='transpose',
            field=models.IntegerField(default=0),
        ),
    ]
