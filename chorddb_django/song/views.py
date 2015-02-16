from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, FormView, DetailView, TemplateView, RedirectView)

from chorddb.tab import parse_tablature, transpose_tablature
from chorddb.chords.library import ChordLibrary

from .forms import InstrumentSelectForm, SongForm, CapoTransposeForm
from .html_render import render_tablature
from .models import Song, SongVersion, InstrumentModel


class HomeView(TemplateView):
    template_name = 'song/home.html'


class SongListView(ListView):
    model = Song


def _render_tablature(tablature, instrument, capo, transpose):
    tab = parse_tablature(tablature.splitlines())
    tab = transpose_tablature(tab, transpose)
    instrument = instrument.capo(capo)
    chords = set()
    for line in tab.lines:
        if line.type == 'chord':
            chords.update(pc.chord for pc in line.data.chords)

    library = ChordLibrary(instrument)

    return render_tablature(tab, {
        c: library.get(c) for c in chords
    })



class SongRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'song_song_instrument_detail'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['instrument_name'] = 'Mimi'
        return super(SongRedirectView,
                     self).get_redirect_url(*args, **kwargs)


class SongInstrumentRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'song_songversion_detail'

    def get_redirect_url(self, *args, **kwargs):
        print "get_red_url"
        song = get_object_or_404(Song, id=kwargs['song_id'])
        print "song", song
        instrument = get_object_or_404(InstrumentModel,
                                       name=kwargs['instrument_name'])
        print "instrument", instrument
        version, _created = song.songversion_set.get_or_create(
            instrument=instrument)
        return super(SongInstrumentRedirectView,
                     self).get_redirect_url(version.id)


class SongVersionDetailView(DetailView):
    model = SongVersion
    pk_url_kwarg = 'songversion_id'
    template_name = 'song/song_detail.html'

    def get_context_data(self, **kwargs):
        form_data = {k : self.request.GET.get(k, v)
                     for k, v in CapoTransposeForm.EMPTY_DATA.items()}
        capo_transpose_form = CapoTransposeForm(form_data)
        data = (capo_transpose_form.cleaned_data
                if capo_transpose_form.is_valid()
                else CapoTransposeForm.EMPTY_DATA)

        lines = _render_tablature(self.object.song.tablature,
                                  self.object.instrument.get_instrument(),
                                  data['capo'],
                                  data['transpose'])

        form = InstrumentSelectForm(initial={
            'name': self.object.instrument.name,
        })

        context = super(SongVersionDetailView, self).get_context_data(**kwargs)
        context.update({
            'lines': lines,
            'instrument_name': self.object.instrument.name,
            'instrument_select_form': form,
            'capo_transpose_form': capo_transpose_form,
            'song': self.object.song,
        })
        return context


class SongAddView(FormView):
    form_class = SongForm
    template_name = "song/song_add.html"

    def form_valid(self, form):
        form.save()
        return redirect('song_song_view', form.instance.id)
