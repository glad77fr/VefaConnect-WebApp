from django import forms
from .models import FollowedProgram
from .models import RealEstateProgram, Address,RealEstateDeveloper, Country,City, State

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


class RealEstateProgramForm(forms.ModelForm):
    class Meta:
        model = RealEstateProgram
        fields = ['name', 'description', 'developer', 'end_date', 'image', 'validated']

    address = forms.ModelChoiceField(Address.objects.all(), required=False, widget=forms.HiddenInput())
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'), 
                                     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_country'}))
                                     
    
    city = forms.ModelChoiceField(queryset=City.objects.all().none(),
                                  widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_city'}))
    
    states = forms.ModelChoiceField(queryset=State.objects.none(),  # Aucun état initialement
        widget=forms.Select(attrs={'class': 'form-control select2','id':'id_states'}),
        required=False)
                                    
    street = forms.CharField()
    developer = forms.ModelChoiceField(queryset=RealEstateDeveloper.objects.all().order_by('name'), 
                                       widget=forms.Select(attrs={'class': 'form-control custom-select'}))

    def save(self, commit=True):
        program = super().save(commit=False)

        if program.validated:
            address = Address.objects.create(
                country=self.cleaned_data.get('country'),
                city=self.cleaned_data.get('city'),
                street=self.cleaned_data.get('street')
            )
            program.address = address

        if commit:  
            program.save()
        return program
