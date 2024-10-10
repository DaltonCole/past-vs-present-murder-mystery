from django import forms
from django.contrib.auth.models import User

from .models import Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = '__all__'
        exclude = ['username']

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude yourself and admin from possible matches
        self.fields['prefered_partner'].queryset = User.objects.all().exclude(id=user_id).exclude(username='admin')
