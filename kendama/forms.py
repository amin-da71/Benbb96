from django import forms

from base.widgets import FirebaseUploadWidget
from kendama.models import Kendama, TrickPlayer


class KendamaForm(forms.ModelForm):
    class Meta:
        model = Kendama
        fields = '__all__'
        widgets = {'photo': FirebaseUploadWidget(folder='kendamas')}


class TrickPlayerForm(forms.ModelForm):
    frequency = forms.ChoiceField(
        choices=tuple([('', '------')] + list(TrickPlayer.FREQUENCY))
    )

    class Meta:
        model = TrickPlayer
        fields = ('frequency',)
