from django import forms
from .models import FollowedProgram

class FollowedProgramForm(forms.ModelForm):
    IS_OWNER_CHOICES = [
        (False, 'Non'),
        (True, 'Oui'),
    ]
    is_owner = forms.ChoiceField(label="J'ai réservé un appartement ou un lot", choices=IS_OWNER_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_is_owner'}))
    apartment_lot_reference = forms.CharField(label="Référence du lot réservé dans le programme (ex: A43)",required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_lot'}))

    class Meta:
        model = FollowedProgram
        fields = ['real_estate_program', 'user_profile', 'is_owner', 'apartment_lot_reference']
 

    def __init__(self, *args, **kwargs):
        self.program = kwargs.pop('program', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['real_estate_program'].initial = self.program
        self.fields['user_profile'].initial = self.user
        self.fields['real_estate_program'].widget = forms.HiddenInput()
        self.fields['user_profile'].widget = forms.HiddenInput()

