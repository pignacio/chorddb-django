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


def _render_tablature(songversion):
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

    library = ChordLibrary(instrument)

    return render_tablature(tablature, {
        c: songversion.chord_versions.get(c.text(), library.get(c))
        for c in chords
    })


class SongRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'song_song_instrument_detail'

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
        lines = _render_tablature(self.object)

        form = InstrumentSelectForm(initial={
            'name': self.object.instrument.name,
        })
        capo_transpose_form = CapoTransposeForm(initial={
            'capo': self.object.capo,
            'transpose': self.object.transpose,
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
