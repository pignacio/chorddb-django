#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import collections
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView, FormView, DetailView, TemplateView,
                                  RedirectView, CreateView, UpdateView)

from chorddb.tab import parse_tablature, transpose_tablature
from chorddb.chords.library import ChordLibrary

from .forms import (
    InstrumentSelectForm, SongForm, CapoTransposeForm, ChordVersionsForm)
from .html_render import render_tablature
from .models import Song, SongVersion, InstrumentModel


class HomeView(TemplateView):
    template_name = 'song/home.html'


class SongListView(ListView):
    model = Song


TablatureData = collections.namedtuple('TablatureData', ['lines', 'chord_versions'])


class SongRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'song:instrument_detail'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['instrument_name'] = 'Mimi'
        return super(SongRedirectView,
                     self).get_redirect_url(*args, **kwargs)


class SongVersionDetailView(DetailView):
    model = SongVersion
    pk_url_kwarg = 'songversion_id'
    template_name = 'song/song_detail.html'

    def _get_songversion_from_params(self, request, *args, **kwargs):
        song = get_object_or_404(Song, id=kwargs['song_id'])
        instrument = get_object_or_404(InstrumentModel,
                                       name=kwargs['instrument_name'])

        form_data = {k : self.request.GET.get(k, v)
                     for k, v in CapoTransposeForm.EMPTY_DATA.items()}
        capo_transpose_form = CapoTransposeForm(form_data)
        data = (capo_transpose_form.cleaned_data
                if capo_transpose_form.is_valid()
                else CapoTransposeForm.EMPTY_DATA)


        version_args = dict(
            song=song,
            instrument=instrument,
            capo=data['capo'],
            transpose=data['transpose']
        )
        try:
            version = SongVersion.objects.get(**version_args)
        except SongVersion.DoesNotExist:
            version = SongVersion(**version_args)
        return version


    def dispatch(self, request, *args, **kwargs):
        if not self.pk_url_kwarg in kwargs:
            version = self._get_songversion_from_params(request, *args,
                                                        **kwargs)
            if version.pk:
                return redirect(version.get_absolute_url())
            else:
                self.__unsaved_version = version
        else:
            self.__unsaved_version = None

        return super(SongVersionDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return (self.__unsaved_version if self.__unsaved_version
                else super(SongVersionDetailView, self).get_object(queryset))

    def get_context_data(self, **kwargs):
        data = self._render_tablature()

        form = InstrumentSelectForm(initial={
            'name': self.object.instrument.name,
        })
        capo_transpose_form = CapoTransposeForm(initial={
            'capo': self.object.capo,
            'transpose': self.object.transpose,
        })
        chord_versions_form = ChordVersionsForm({
            c: self.object.chord_versions.get(c.text(), None)
            for c in data.chord_versions
        })

        context = super(SongVersionDetailView, self).get_context_data(**kwargs)
        context.update({
            'lines': data.lines,
            'instrument_name': self.object.instrument.name,
            'instrument_select_form': form,
            'capo_transpose_form': capo_transpose_form,
            'chord_versions_form': chord_versions_form,
            'song': self.object.song,
            'chord_versions': json.dumps(
                {k.text(): [str(v) for v in vv]
                 for k, vv in data.chord_versions.items()},
                indent=1)
        })
        return context

    def _render_tablature(self):
        songversion = self.object
        tablature = parse_tablature(songversion.song.tablature.splitlines())
        instrument = songversion.instrument.get_instrument()
        if songversion.transpose:
            tablature = transpose_tablature(tablature, songversion.transpose)
        if songversion.capo:
            instrument = instrument.capo(songversion.capo)
        chords = set()
        for line in tablature.lines:
            if line.type == 'chord':
                chords.update(pc.chord for pc in line.data.chords)
        request_versions = ChordVersionsForm(chords, self.request.GET).get_chord_versions()

        library = ChordLibrary(instrument)

        library_versions = {
            c: [str(v) for v in library.get_all(c)] for c in chords
        }

        tab_versions = {}
        for chord in chords:
            preferred = request_versions.get(
                chord, songversion.chord_versions.get(chord.text(), None))
            if preferred:
                if not preferred in library_versions[chord]:
                    library_versions[chord].append(preferred)
                tab_versions[chord] = preferred
            elif library_versions[chord]:
                tab_versions[chord] = library_versions[chord][0]


        return TablatureData(lines=render_tablature(tablature, tab_versions),
                             chord_versions=library_versions)


class SongAddView(CreateView):
    model = Song
    form_class = SongForm
    template_name_suffix = "_add"


class SongUpdateView(UpdateView):
    model = Song
    form_class = SongForm
    pk_url_kwarg = 'song_id'
    template_name_suffix = "_update"


class SelectedChordPadView(TemplateView):
    template_name = 'song/layout/selected_chord_pad.html'

    def get_context_data(self):
        data = super(SelectedChordPadView, self).get_context_data()
        data.update({
            k: self.request.GET.get(k, "???")
            for k in ['chord', 'fingering', 'total', 'index', 'chord_id']
        })
        return data

def update_song_version(request, song_id, instrument_name):
    song = get_object_or_404(Song, id=song_id)
    instrument = get_object_or_404(InstrumentModel, name=instrument_name)
    capo = request.GET.get('capo', 0)
    transpose = request.GET.get('transpose', 0)
    songversion, _created = SongVersion.objects.get_or_create(
        song=song,
        instrument=instrument,
        capo=capo,
        transpose=transpose,
    )
    chords = set()
    tablature = parse_tablature(song.tablature.splitlines())
    for line in tablature.lines:
        if line.type == 'chord':
            chords.update(pc.chord for pc in line.data.chords)
    versions = ChordVersionsForm(chords, request.GET).get_chord_versions()
    songversion.chord_versions = {
        c.text(): f for c, f in versions.items()
    };
    songversion.save()
    return redirect(songversion.get_absolute_url())

