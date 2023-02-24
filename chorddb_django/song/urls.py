#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long


import logging

from django.urls import re_path

from .views import (
    SongListView, SongAddView, SongVersionDetailView, SongRedirectView,
    HomeView, SelectedChordPadView, update_song_version
)


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = [  # pylint: disable=invalid-name
    re_path(r'^/?$', HomeView.as_view(), name='song_home'),
    re_path(r'^song/?$', SongListView.as_view(), name='song_song_list'),
    re_path(r'^song/add/?$', SongAddView.as_view(), name='song_song_add'),
    re_path(r'^song/(?P<song_id>\d+)/?$', SongRedirectView.as_view(), name='song_song_detail'),
    re_path(r'^song/(?P<song_id>\d+)/(?P<instrument_name>\w+)/?$', SongVersionDetailView.as_view(), name='song_song_instrument_detail'),
    re_path(r'^song/(?P<song_id>\d+)/(?P<instrument_name>\w+)/save/?$', update_song_version, name='song_song_instrument_save'),
    re_path(r'^song/version/(?P<songversion_id>\d+)/?$', SongVersionDetailView.as_view(), name='song_songversion_detail'),
    re_path(r'^layout/selected_chord_pad/?$', SelectedChordPadView.as_view(), name='song_selected_chord_pad'),
]
