from django import forms

class OnOffSwitchForm(forms.Form):
    switch = forms.BooleanField(required=False)