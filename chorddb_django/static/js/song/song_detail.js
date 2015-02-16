/* jshint browser: true, jquery: true */
/* global songUrl */

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

function reloadTab() {
  var url = window.location.pathname;
  var qstring = $('#form_capo_transpose').serialize();
  url += '?' + qstring;
  window.location.hash = '#' + qstring;
  $('#tab').load(url + ' #tab pre');
  clearSelectedChord();
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
    clearSelectedChord();
    var selected = $(this);
    $('#selected-chord').text(selected.attr('chord') + '(' +
      selected.attr('fingering') +')');
    selected.addClass('tab-chord-selected');
  });
});
