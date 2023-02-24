#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long


import logging

from django.conf.urls import patterns, url

from .views import (
    SongListView, SongAddView, SongVersionDetailView, SongRedirectView,
    HomeView, SelectedChordPadView
)


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = patterns(  # pylint: disable=invalid-name
    'song.views',
    url(r'^/?$', HomeView.as_view(), name='song_home'),
    url(r'^song/?$', SongListView.as_view(), name='song_song_list'),
    url(r'^song/add/?$', SongAddView.as_view(), name='song_song_add'),
    url(r'^song/(?P<song_id>\d+)/?$', SongRedirectView.as_view(), name='song_song_detail'),
    url(r'^song/(?P<song_id>\d+)/(?P<instrument_name>\w+)/?$', SongVersionDetailView.as_view(), name='song_song_instrument_detail'),
    url(r'^song/(?P<song_id>\d+)/(?P<instrument_name>\w+)/save/?$', 'update_song_version', name='song_song_instrument_save'),
    url(r'^song/version/(?P<songversion_id>\d+)/?$', SongVersionDetailView.as_view(), name='song_songversion_detail'),
    url(r'^layout/selected_chord_pad/?$', SelectedChordPadView.as_view(), name='song_selected_chord_pad'),
)
