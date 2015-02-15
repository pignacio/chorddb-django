#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals

import logging

from django.conf.urls import patterns, url

from .views import SongListView, SongAddView, SongDetailView, HomeView


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = patterns(  # pylint: disable=invalid-name
    'song.views',
    url(r'^/?$', HomeView.as_view(), name='song_home'),
    url(r'^song/?$', SongListView.as_view(), name='song_song_list'),
    url(r'^song/add/?$', SongAddView.as_view(), name='song_song_add'),
    url(r'^song/(?P<song_id>\d+)/?$', SongDetailView.as_view(), name='song_song_view'),
    url(r'^song/(?P<song_id>\d+)/(?P<instrument_name>\w+)/?$', SongDetailView.as_view(), name='song_song_view_instrument'),
)
