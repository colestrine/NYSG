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

class ModeForm(forms.Form):
	mode = forms.ChoiceField(required=False, choices=[('machine_learning', 'Machine Learning'), ('manual', 'Manual')], widget=forms.Select(attrs={'onchange': 'mode_form.submit();'}))

class ActionForm(forms.Form):
	actions = [('none', '0 sec'), ('big_decrease', '15 sec'), ('small_decrease', '30 sec'), ('small_increase', '45 sec'), ('big_increase', '60 sec')]
	water = forms.ChoiceField(required=True, choices=actions, label="Water", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))
	fan = forms.ChoiceField(required=True, choices=actions, label="Fan", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))
	heat = forms.ChoiceField(required=True, choices=actions, label="Heat", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))
	light = forms.ChoiceField(required=True, choices=actions, label="Light", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))

class AlertForm(forms.Form):
	detail_levels = [('high', 'high detail'), ('low', 'low detail')]
	rate_levels = [('day', "daily"), ('hour', 'hourly'), ('minute', "by the minute")]
	detail = forms.ChoiceField(required=True, choices=detail_levels, label="Detail", widget=forms.Select(attrs={'onchange': 'alert_form.submit();'}))
	rate = forms.ChoiceField(required=True, choices=rate_levels, label="Rate", widget=forms.Select(attrs={'onchange': 'alert_form.submit();'}))
	
class PwmForm(forms.Form):
	dc_levels = [(str(i), str(i) + "% Duty Cycles") for i in range(0, 101, 10)]
	fan_dc = forms.ChoiceField(required=True, choices=dc_levels, label="Fan Duty Cycles", widget=forms.Select(attrs={'onchange': 'pwm_form.submit();'}))
	light_dc = forms.ChoiceField(required=True, choices=dc_levels, label="Light Duty Cycles", widget=forms.Select(attrs={'onchange': 'pwm_form.submit();'}))
	