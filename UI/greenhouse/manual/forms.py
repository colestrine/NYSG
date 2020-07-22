from django import forms
from scripts.data_handler import data_handler

class ActionForm(forms.Form):
	actions = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
	water = forms.ChoiceField(required=True, choices=actions, label="Water", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))
	fan = forms.ChoiceField(required=True, choices=actions, label="Fan", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))
	heat = forms.ChoiceField(required=True, choices=actions, label="Heat", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))
	light = forms.ChoiceField(required=True, choices=actions, label="Light", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))