from django import forms
from scripts.data_handler import data_handler

class PlantProfileForm(forms.Form):
	plant_profile_choices = [("Custom", "Custom")]
	profiles = data_handler.get_available_profiles()
	for profile in profiles:
		plant_profile_choices.append(profile)

	plant_profile = forms.ChoiceField(required=False, choices=plant_profile_choices, widget=forms.Select(attrs={'onchange': 'plant_profile_form.submit();'}))

class HealthyLevelsForm(forms.Form):
	temperature_choices = data_handler.get_available_temperatures()
	humidity_choices = data_handler.get_available_humidities()
	soil_moisture_choices = data_handler.get_available_soil_moistures() #[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
	sunlight_choices = data_handler.get_available_sunlights() #[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]

	healthy_levels = data_handler.read_healthy_levels()

	temperature = forms.ChoiceField(required=False, choices=temperature_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	humidity = forms.ChoiceField(required=False, choices=humidity_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	soil_moisture = forms.ChoiceField(required=False, label="Soil Moisture", choices=soil_moisture_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	sunlight = forms.ChoiceField(required=False, choices=sunlight_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))