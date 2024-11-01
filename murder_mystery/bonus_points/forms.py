from django import forms

from teams.models import Team

class BonusPointForm(forms.Form):
    answer = forms.CharField(
            label='Answer',
            max_length=100,
            )

class AdminBonusPointForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    amount = forms.IntegerField()
    reason = forms.CharField()
