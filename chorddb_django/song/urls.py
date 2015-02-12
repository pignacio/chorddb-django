#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import patterns, include, url

import logging


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = patterns(
    'song.views',
    url(r'^/?$', 'home', name='song_home'),
    url(r'^song/?$', 'song_list', name='song_song_list'),
    url(r'^song/add/?$', 'song_add', name='song_song_add'),
    url(r'^song/(?P<song_id>\d+)/?$', 'song_view', name='song_song_view'),
    url(r'^song/(?P<song_id>\d+)/(?P<instrument_name>\w+)/?$', 'song_view', name='song_song_view_instrument'),
)
