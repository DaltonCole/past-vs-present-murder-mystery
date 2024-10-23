from django import forms

class BonusPointForm(forms.Form):
    answer = forms.CharField(
            label='Answer',
            max_length=100,
            )
