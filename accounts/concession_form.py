from django import forms
from .models import ConcessionData

class ConcessionDataForm(forms.ModelForm):
    b_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(choices=[('Male','Male'), ('Female','Female'), ('Other','Other')], required=False)

    class Meta:
        model = ConcessionData
        fields = [
            's_name', 'b_date', 'age', 'gender', 'department', 
            'address', 'adhar_no', 'phone_no', 'destination', 'duration'
        ]
