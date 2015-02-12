from __future__ import  unicode_literals
from django.db import models


class Song(models.Model):
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    tablature = models.TextField()

    def __unicode__(self):
        return "Song: {s.artist} - {s.title}".format(s=self)


class SongVersion(models.Model):
    song = models.ForeignKey('Song')
    instrument = models.ForeignKey('InstrumentModel')
#      chord_versions = models.TextField() # Json or HStore
#      special_chords = models.TextField() # Json or Array<HStore>


class InstrumentModel(models.Model):
    name = models.CharField(max_length=255)
    definition = models.CharField(max_length=255)

    def __unicode__(self):
        return "InstrumentModel: {s.name} : '{s.definition}'".format(s=self)
