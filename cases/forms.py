from django import forms
from .models import MissingPerson

class MissingPersonForm(forms.ModelForm):
    class Meta:
        model = MissingPerson
        fields = [
            'name', 
            'age', 
            'gender', 
            'height', 
            'description', 
            'language', 
            'city', 
            'photo', 
            'case_registered_by', 
            'phone_number', 
            'email', 
            'address'
        ]
