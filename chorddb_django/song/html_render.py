#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from StringIO import StringIO
import collections
import logging


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


FingeredChord = collections.namedtuple('Fingeredchord', ['chord', 'fingering'])



def render_tablature(tablature, chord_versions=None, debug=False):
    chord_versions = chord_versions or {}
    res = []
    for line in tablature.lines:
        if line.type == 'chord':
            lip = LineInProgress()
            for poschord in line.data.chords:
                write_span_with_class(lip, poschord.chord.text(),
                                      poschord.position, 'chord')
                version = chord_versions.get(poschord.chord, None)
                if version:
                    write_span_with_class(lip, "({})".format(version),
                                          poschord.position, 'fingering')
                lip.write_at(" ", poschord.position)
            res.append(lip.getvalue())
        else:
            res.append(line.original)
    return res

def write_span_with_class(lip, text, position, style):
    return lip.write_at(text, position, '<span class="{}">'.format(style),
                        '</span>')



class LineInProgress(object):
    def __init__(self):
        self._string = StringIO()
        self._size = 0

    def write_at(self, text, position=0, wrap_left='', wrap_right=''):
        if self._size <= position:
            self._string.write(" " * (position - self._size))
            self._size = position
        self._string.write(wrap_left)
        self._string.write(text)
        self._string.write(wrap_right)
        self._size += len(text)
        print "Write at: ", self._string.getvalue()

    def getvalue(self):
        return self._string.getvalue()
