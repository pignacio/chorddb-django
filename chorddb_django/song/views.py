from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, DetailView, TemplateView

from chorddb.tab.parser import parse_tablature
from chorddb.chords.library import ChordLibrary
from chorddb.instrument import GUITAR, LOOG, UKELELE

from .forms import InstrumentSelectForm, SongForm
from .html_render import render_tablature
from .models import Song


_INSTRUMENTS = {
    'guitar': GUITAR,
    'ukelele': UKELELE,
    'loog': LOOG,
}


class HomeView(TemplateView):
    template_name = 'song/home.html'


class SongListView(ListView):
    model = Song


def _render_tablature(tablature, instrument):
    tab = parse_tablature(tablature.splitlines())
    chords = set()
    for line in tab.lines:
        if line.type == 'chord':
            chords.update(pc.chord for pc in line.data.chords)

    library = ChordLibrary(instrument)

    return render_tablature(tab, {
        c: library.get(c) for c in chords
    })


class SongDetailView(DetailView):
    model = Song
    pk_url_kwarg = 'song_id'

    def get_context_data(self, **kwargs):
        instrument_name = self.kwargs.get('instrument_name', None)
        try:
            instrument = _INSTRUMENTS[instrument_name]
        except KeyError:
            instrument = GUITAR
            instrument_name = 'guitar'

        lines = _render_tablature(self.object.tablature, instrument)

        form = InstrumentSelectForm(initial={
            'name': instrument_name,
        })

        context = super(SongDetailView, self).get_context_data(**kwargs)
        context.update({
            'lines': lines,
            'instrument_name': instrument_name,
            'instrument_select_form': form,
        })
        return context


class SongAddView(FormView):
    form_class = SongForm
    template_name = "song/song_add.html"

    def form_valid(self, form):
        form.save()
        return redirect('song_song_view', form.instance.id)
