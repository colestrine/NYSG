from django import forms
from scripts.data_handler import data_handler

class PlantProfileForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		plant_profile_choices = [("Custom", "Custom")]
		profiles = data_handler.get_available_profiles()
		for profile in profiles:
			plant_profile_choices.append(profile)
		self.fields['plant_profile'].choices = plant_profile_choices

	plant_profile = forms.ChoiceField(required=False, label="Plant Profile", widget=forms.Select(attrs={'onchange': 'plant_profile_form.submit();'}))

class HealthyLevelsForm(forms.Form):
	temperature_choices = data_handler.get_available_temperatures()
	humidity_choices = data_handler.get_available_humidities()
	soil_moisture_choices = data_handler.get_available_soil_moistures()
	sunlight_choices = data_handler.get_available_sunlights()

	temperature = forms.ChoiceField(required=False, choices=temperature_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	humidity = forms.ChoiceField(required=False, choices=humidity_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	soil_moisture = forms.ChoiceField(required=False, label="Soil Moisture", choices=soil_moisture_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	sunlight = forms.ChoiceField(required=False, choices=sunlight_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))

class SaveProfileForm(forms.Form):
	temperature_choices = data_handler.get_available_temperatures()
	humidity_choices = data_handler.get_available_humidities()
	soil_moisture_choices = data_handler.get_available_soil_moistures()
	sunlight_choices = data_handler.get_available_sunlights()

	custom_temperature = forms.ChoiceField(required=False, choices=temperature_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	custom_humidity = forms.ChoiceField(required=False, choices=humidity_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	custom_soil_moisture = forms.ChoiceField(required=False, label="Soil Moisture", choices=soil_moisture_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	custom_sunlight = forms.ChoiceField(required=False, choices=sunlight_choices, widget=forms.Select(attrs={'onchange': 'healthy_levels_form.submit();'}))
	profile_name = forms.CharField(max_length=100, label="Profile Name")