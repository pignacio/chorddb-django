from __future__ import  unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

from chorddb.instrument import GUITAR, LOOG, UKELELE


class Song(models.Model):
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    tablature = models.TextField()

    def __unicode__(self):
        return "Song: {s.artist} - {s.title}".format(s=self)

    def get_absolute_url(self):
        return reverse('song_song_detail', kwargs={'song_id': self.id})


class SongVersion(models.Model):
    song = models.ForeignKey('Song')
    instrument = models.ForeignKey('InstrumentModel')
#      chord_versions = models.TextField() # Json or HStore
#      special_chords = models.TextField() # Json or Array<HStore>

    def __unicode__(self):
        return 'SongVersion: {s.song.title} for {s.instrument.name}'.format(
            s=self)

    def get_absolute_url(self):
        return reverse('song_songversion_detail',
                       kwargs={'songversion_id': self.id})


class InstrumentModel(models.Model):
    name = models.CharField(max_length=255)
    definition = models.CharField(max_length=255)

    _NAMED_INSTRUMENTS = {i.name: i for i in [GUITAR, LOOG, UKELELE]}

    def __unicode__(self):
        return "InstrumentModel: {s.name} : '{s.definition}'".format(s=self)

    def get_instrument(self):
        return self._NAMED_INSTRUMENTS[self.definition]
