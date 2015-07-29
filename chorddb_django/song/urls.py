#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals

import logging

from django.conf.urls import patterns, url

from .views import (
    SongListView, SongAddView, SongVersionDetailView, SongRedirectView,
    HomeView, SelectedChordPadView
)


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = patterns(  # pylint: disable=invalid-name
    'song.views',
    url(r'^$', SongListView.as_view(), name='list'),
    url(r'^add$', SongAddView.as_view(), name='add'),
    url(r'^(?P<song_id>\d+)$', SongRedirectView.as_view(), name='detail'),
    url(r'^(?P<song_id>\d+)/(?P<instrument_name>\w+)$', SongVersionDetailView.as_view(), name='instrument_detail'),
    url(r'^(?P<song_id>\d+)/(?P<instrument_name>\w+)/save$', 'update_song_version', name='instrument_save'),
    url(r'^version/(?P<songversion_id>\d+)$', SongVersionDetailView.as_view(), name='songversion_detail'),
    url(r'^selected_chord_pad$', SelectedChordPadView.as_view(), name='selected_chord_pad'),
)
