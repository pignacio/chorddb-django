#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext as _

import floppyforms.__future__ as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from .models import Song, InstrumentModel


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class InstrumentSelectForm(forms.Form):
    name = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(InstrumentSelectForm, self).__init__(*args, **kwargs)
        self.fields['name'].choices = [
            (i.name, i.name) for i in InstrumentModel.objects.all()
        ]
        self.helper = FormHelper()
        self.helper.form_id = 'form_select_instrument'
        self.helper.form_class = 'form-inline'
        self.helper.form_show_labels = False


class CapoTransposeForm(forms.Form):
    capo = forms.TypedChoiceField(
        choices=[(n, "{}".format(n)) for n in xrange(13)],
        coerce=int, empty_value=0, required=False, initial=0)
    transpose = forms.TypedChoiceField(
        choices=[(n, "{}".format(n)) for n in xrange(-12, 13)],
        coerce=int, empty_value=0, required=False, initial=0)

    EMPTY_DATA = {
        'capo': 0,
        'transpose': 0,
    }

    def __init__(self, *args, **kwargs):
        super(CapoTransposeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form_capo_transpose'
        self.helper.form_class = 'form-inline'
        self.helper.disable_csrf = True


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = (
            'artist',
            'title',
            'tablature',
        )

    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Fieldset(
                _('Metadata'),
                'artist',
                'title',
            ),
            Fieldset(
                _('Tablature'),
                'tablature',
            ),
            FormActions(
                Submit(
                    'submit',
                    _('Save'),
                    css_class='btn-primary pull-right',
                    data_loading_text=_('Saving...')
                ),
            ),
        )


class ChordVersionsForm(forms.Form):
    def __init__(self, chords, *args, **kwargs):
        super(ChordVersionsForm, self).__init__(*args, **kwargs)
        self._chords = chords
        for chord in chords:
            self.fields[self.field_id(chord)] = forms.CharField(
                required=False, widget=forms.HiddenInput(),
                initial=self.get_initial(chords, chord))
        self.helper = FormHelper()
        self.helper.form_id = 'form_chord_versions'
        self.helper.disable_csrf = True

    @staticmethod
    def field_id(chord):
        return 'chord_version_{}'.format(chord.text())

    @staticmethod
    def get_initial(chords, chord):
        try:
            return chords[chord]
        except Exception:
            return None

    def get_chord_versions(self):
        self.is_valid()
        values = {
            c: self.cleaned_data[self.field_id(c)] for c in self._chords
        }
        return {k: v for k, v in values.items() if v}



