/* jshint browser: true, jquery: true */
/* global songUrl,selectedChordPadUrl,chordVersions */

var isModified = false;

function leavePage(destination) {
  window.location = destination;
}

function switchInstrument() {
  var url = songUrl + '/' + $('#id_name').val();
  leavePage(url);
}

function switchVersion() {
  var url = songUrl + '/' + $('#id_name').val();
  url += '?' + $('#id_capo,#id_transpose').serialize();
  leavePage(url);
}

function clearSelectedChord() {
    $('#selected-chord').text('');
    $('.tab-chord').removeClass('tab-chord-selected');
}

function updateSelectedChord(chordId) {
  clearSelectedChord();
  var selected = $('#chord-' + chordId);
  var chord = selected.attr('chord');
  var versions = chordVersions[chord];
  var fingering = selected.attr('fingering');
  $('#selected-chord').load(selectedChordPadUrl + '?' + $.param({
    chord: chord,
    fingering: fingering,
    total: versions.length,
    index: versions.indexOf(fingering) + 1,
    chord_id: selected.attr('chord-id'),
  }), function() {
    selected.addClass('tab-chord-selected');
  });
}

function updateTab(chordId) {
  var url = window.location.pathname;
  var qstring = $('#form_capo_transpose').serialize();
  qstring += '&' + $('#form_chord_versions :input[value]').serialize();
  url += '?' + qstring;
  window.location.hash = '#' + qstring;
  $('#tab').load(url + ' #tab pre', function() {
    $('.tab-chord').click(function() {
      updateSelectedChord($(this).attr('chord-id'));
    });
    updateSelectedChord(chordId);
  });
}

function moveSelectedChord(chordId, interval) {
  var selected = $('#chord-' + chordId);
  var chord = selected.attr('chord');
  var current = selected.attr('fingering');
  var index = chordVersions[chord].indexOf(current);
  var newIndex = (index + interval) % chordVersions[chord].length;
  var newFingering = chordVersions[chord][newIndex];
  $('#id_chord_version_' + chord).val(newFingering);
  updateTab(chordId);
  $('#save-warning').show();
}

function selectedChordNext(chordId) {
  moveSelectedChord(chordId, 1);
}

function selectedChordPrev(chordId) {
  moveSelectedChord(chordId, -1);
}

function saveSongVersion() {
  var url = songUrl + '/' + $('#id_name').val() + '/save/?';
  url += $('#form_capo_transpose').serialize() + '&';
  url += $('#form_chord_versions').serialize();
  window.location = url;
}

$(document).ready(function() {
  $('#id_name').on('change', function() {
    switchInstrument();
  });
  $('#id_capo').on('change', function() {
    switchVersion();
  });
  $('#id_transpose').on('change', function() {
    switchVersion();
  });
  $('.tab-chord').click(function() {
    updateSelectedChord($(this).attr('chord-id'));
  });
});
