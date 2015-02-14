from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, DetailView, TemplateView

from chorddb.tab import parse_tablature, transpose_tablature
from chorddb.chords.library import ChordLibrary
from chorddb.instrument import GUITAR, LOOG, UKELELE

from .forms import InstrumentSelectForm, SongForm, CapoTransposeForm
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
        form_data = {k : self.request.GET.get(k, v)
                     for k, v in CapoTransposeForm.EMPTY_DATA.items()}
        capo_transpose_form = CapoTransposeForm(form_data)
        data = (capo_transpose_form.cleaned_data
                if capo_transpose_form.is_valid()
                else CapoTransposeForm.EMPTY_DATA)

        lines = _render_tablature(self.object.tablature, instrument,
                                  data['capo'],
                                  data['transpose'])

        form = InstrumentSelectForm(initial={
            'name': instrument_name,
        })

        context = super(SongDetailView, self).get_context_data(**kwargs)
        context.update({
            'lines': lines,
            'instrument_name': instrument_name,
            'instrument_select_form': form,
            'capo_transpose_form': capo_transpose_form,
        })
        return context


class SongAddView(FormView):
    form_class = SongForm
    template_name = "song/song_add.html"

    def form_valid(self, form):
        form.save()
        return redirect('song_song_view', form.instance.id)
