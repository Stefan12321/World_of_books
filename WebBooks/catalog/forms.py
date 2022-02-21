from django import forms
from django.forms import ModelForm
from datetime import date
from .models import Book
from django.core.exceptions import ValidationError


class AuthorsForm(forms.Form):
    first_name = forms.CharField(label="Author first name")
    last_name = forms.CharField(label="Author last_name name")
    date_of_birth = forms.DateField(label="Birth date",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(label="Death date",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']
