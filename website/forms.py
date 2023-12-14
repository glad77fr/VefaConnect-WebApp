from django import forms
from .models import FollowedProgram
from .models import RealEstateProgram, Address,RealEstateDeveloper, Country,City, State
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib import messages

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
        fields = ['name', 'description', 'developer','image', 'end_date', 'validated']

    address = forms.ModelChoiceField(Address.objects.all(), required=False, widget=forms.HiddenInput())
    image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'), 
                                     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_country'}))
                                     
    
    city = forms.ModelChoiceField(queryset=City.objects.all().order_by('name').none(),
                                  widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_city'}))
    
    states = forms.ModelChoiceField(queryset=State.objects.all().order_by('name').none(),  # Aucun état initialement
        widget=forms.Select(attrs={'class': 'form-control select2','id':'id_states'}),
        required=False)
                                    
    street = forms.CharField()
    developer = forms.ModelChoiceField(queryset=RealEstateDeveloper.objects.all().order_by('name'), 
                                       widget=forms.Select(attrs={'class': 'form-control custom-select'}))
    def clean(self):
        cleaned_data = super().clean()
        city_id = cleaned_data.get("city")
        state_id = cleaned_data.get("states")

        # Vérifier si city_id correspond à un objet City valide
        if city_id and not isinstance(city_id, City):
            raise ValidationError({'city': "Select a valid choice. That choice is not one of the available choices."})

        # Faire de même pour states
        if state_id  and not isinstance(state_id, State):
            raise ValidationError({'states': "Select a valid choice. That choice is not one of the available choices."})
        return cleaned_data

    def save(self, commit=True):
        print("Début de la méthode save")

        # Vérification de la conformité de l'adresse
        country = self.cleaned_data.get('country')
        city = self.cleaned_data.get('city')
        states = self.cleaned_data.get('states')
        street = self.cleaned_data.get('street')

        if not country or not city or not street:
            print("Erreur : Les informations d'adresse sont incomplètes.")
            raise ValidationError("Les informations d'adresse sont incomplètes.")
        print("Informations d'adresse complètes")

        # Préparation de l'adresse
        address = Address(country=country, city=city, state=states, street=street)
        print(f"Adresse préparée : {address}")

        # Sauvegarde du programme avec l'adresse
        program = super().save(commit=False)
        with transaction.atomic():
            print("En cours de sauvegarde de l'adresse et du programme")
            address.save()
            program.address = address
            if commit:
                program.save()
                print("Programme Sauvegardé")
            print("Programme et adresse sauvegardés avec succès")

        print("Fin de la méthode save")
        return program
