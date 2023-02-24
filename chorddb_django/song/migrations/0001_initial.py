# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('definition', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('artist', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('tablature', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SongVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instrument', models.ForeignKey(to='song.InstrumentModel', on_delete=models.CASCADE)),
                ('song', models.ForeignKey(to='song.Song', on_delete=models.CASCADE)),
            ],
        ),
    ]
