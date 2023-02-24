#! /usr/bin/env python
# -*- coding: utf-8 -*-


from io import StringIO
import collections
import logging


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


FingeredChord = collections.namedtuple('Fingeredchord', ['chord', 'fingering'])



def render_tablature(tablature, chord_versions=None, debug=False):
    chord_versions = chord_versions or {}
    res = []
    for line_index, line in enumerate(tablature.lines):
        if line.type == 'chord':
            lip = LineInProgress()
            for chord_index, poschord in enumerate(line.data.chords):
                chord_id = "{}_{}".format(line_index, chord_index)
                container_id = "chord-{}".format(chord_id)
                lip.write_at('', poschord.position)
                version = chord_versions.get(poschord.chord, None)
                lip.hidden_write('<span id="{}" class="tab-chord" chord="{}" '
                                 'fingering="{}" chord-id="{}">'.format(
                                     container_id, poschord.chord.text(),
                                     version if version else "",
                                     chord_id))
                write_span_with_class(lip, poschord.chord.text(),
                                      poschord.position, 'chord')
                if version:
                    write_span_with_class(lip, "({})".format(version),
                                          poschord.position, 'fingering')
                lip.hidden_write("</span>")
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

    def hidden_write(self, text):
        self._string.write(text)

    def getvalue(self):
        return self._string.getvalue()
