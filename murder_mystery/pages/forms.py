import string

from characters.models import Character
from django import forms
from django.contrib.auth.models import User

class LocationClueForm(forms.Form):
    answer = forms.CharField(
            label='Answer',
            widget=forms.Select(choices={letter.lower(): letter.upper() for letter in string.ascii_lowercase})
            )

class CharacterClueForm(forms.Form):
    answer = forms.CharField(
            label='Answer',
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].widget = forms.Select(
                choices={
                    f'{char.id}': f'{char.character_name} - {char.real_name}' for char in Character.objects.all().order_by('character_name')
                    }
                )
