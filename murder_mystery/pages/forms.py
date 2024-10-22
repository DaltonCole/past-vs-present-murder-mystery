import string

from django import forms
from django.contrib.auth.models import User

from characters.models import Character

class VideoClueForm(forms.Form):
    answer = forms.CharField(
            label='Answer',
            widget=forms.Select(choices={letter.lower(): letter.upper() for letter in string.ascii_lowercase})
            )

class TextClueForm(forms.Form):
    answer = forms.CharField(
            label='Answer',
            widget=forms.Select(choices={f'{char.id}': f'{char.character_name} - {char.real_name}' for char in Character.objects.all()})
            )
