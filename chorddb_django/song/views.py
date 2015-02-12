from django.shortcuts import render, get_object_or_404, redirect

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


def home(requst):
    return render(requst, 'song/home.html', {
    })


def song_list(request):
    return render(request, 'song/song_list.html', {
        'songs': Song.objects.all(),
    })


def song_view(request, song_id, instrument_name=None):
    song = get_object_or_404(Song, id=song_id)
    try:
        instrument = _INSTRUMENTS[instrument_name]
    except KeyError:
        instrument = GUITAR
        instrument_name = 'guitar'
    tab = parse_tablature(song.tablature.splitlines())
    chords = set()
    for line in tab.lines:
        if line.type == 'chord':
            chords.update(pc.chord for pc in line.data.chords)

    library = ChordLibrary(instrument)

    lines = render_tablature(tab, {
        c: library.get(c) for c in chords
    })

    form = InstrumentSelectForm(initial={
        'name': instrument_name,
    })

    return render(request, 'song/song_view.html', {
        'song': song,
        'lines': lines,
        'instrument_name': instrument_name,
        'instrument_select_form': form,
    })


def song_add(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('song_song_view', form.instance.id)
    else:
        form = SongForm()
    return render(request, 'song/song_add.html', {
        'form': form,
    }
    )

