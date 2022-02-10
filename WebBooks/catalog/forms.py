from django import forms
from datetime import date

class AuthorsForm(forms.Form):
    first_name = forms.CharField(label="Author first name")
    last_name = forms.CharField(label="Author last_name name")
    date_of_birth = forms.DateField(label="Birth date",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(label="Death date",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
