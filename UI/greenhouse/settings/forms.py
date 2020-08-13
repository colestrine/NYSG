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
	actions = [('off', '0 sec'), ('low', '30 sec'), ('high', '60 sec')]
	water = forms.ChoiceField(required=True, choices=actions, label="Water", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))
	fan = forms.ChoiceField(required=True, choices=actions, label="Fan", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))
	heat = forms.ChoiceField(required=True, choices=actions, label="Heat", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))
	light = forms.ChoiceField(required=True, choices=actions, label="Light", widget=forms.Select(attrs={'onchange': 'action_form.submit();'}))

class AlertForm(forms.Form):
	detail_levels = [('high', 'High Detail'), ('low', 'Low Detail')]
	rate_levels = [('day', "Daily"), ('hour', 'Hourly'), ('minute', "Minutely")]
	detail = forms.ChoiceField(required=True, choices=detail_levels, label="Detail", widget=forms.Select(attrs={'onchange': 'alert_form.submit();'}))
	rate = forms.ChoiceField(required=True, choices=rate_levels, label="Rate", widget=forms.Select(attrs={'onchange': 'alert_form.submit();'}))
	email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'onchange': 'alert_form.submit();'}))
	password = forms.CharField(required=False, widget=forms.PasswordInput(render_value=True, attrs={'onchange': 'alert_form.submit();'}))

class PwmForm(forms.Form):
	dc_levels = [(str(i), str(i) + ' %') for i in range(0, 101, 10)]
	fan_dc = forms.ChoiceField(required=True, choices=dc_levels, label="Fan Duty Cycles", widget=forms.Select(attrs={'onchange': 'pwm_form.submit();'}))
	light_dc = forms.ChoiceField(required=True, choices=dc_levels, label="Light Duty Cycles", widget=forms.Select(attrs={'onchange': 'pwm_form.submit();'}))
	
class FreqForm(forms.Form):
	freq_levels = [(str(i), str(i) + " Hz") for i in range(0, 501, 25)]
	fan_freq = forms.ChoiceField(required=True, choices=freq_levels, label="Fan Frequency", widget=forms.Select(attrs={'onchange': 'freq_form.submit();'}))
	light_freq = forms.ChoiceField(required=True, choices=freq_levels, label="Light Frequency", widget=forms.Select(attrs={'onchange': 'freq_form.submit();'}))
	
class UpdateIntervalForm(forms.Form):
	interval_levels = [('60', '1 Minute'), ('120', '2 Minutes'), ('300', '5 Minutes')]
	interval = forms.ChoiceField(required=True, choices=interval_levels, label="Interval Update Period", widget=forms.Select(attrs={'onchange': 'update_interval.submit();'}))
	
class DeleteForm(forms.Form):
	delete_levels = [('no', 'No'),('yes', 'Yes')]
	delete_field = forms.ChoiceField(required=True, choices=delete_levels, label="Delete Data", widget=forms.Select(attrs={'onchange': 'delete_form.submit();'}))
	
class StartDateForm(forms.Form):
	day_levels = [(('0' + str(i), '0' + str(i)) if i < 10 else (str(i), str(i))) for i in range(1, 32)]
	month_levels = [(('0' + str(i), '0' + str(i)) if i < 10 else (str(i), str(i))) for i in range(1, 13)]
	year_levels = [(str(i), str(i)) for i in range(2020, 2101)]
	start_day = forms.ChoiceField(required=True, choices=day_levels, label="Start Day", widget=forms.Select(attrs={'onchange': 'start_date_form.submit();'}))
	start_month = forms.ChoiceField(required=True, choices=month_levels, label="Start Month", widget=forms.Select(attrs={'onchange': 'start_date_form.submit();'}))
	start_year = forms.ChoiceField(required=True, choices=year_levels, label="Start Year", widget=forms.Select(attrs={'onchange': 'start_date_form.submit();'}))
	end_day = forms.ChoiceField(required=True, choices=day_levels, label="End Day", widget=forms.Select(attrs={'onchange': 'start_date_form.submit();'}))
	end_month = forms.ChoiceField(required=True, choices=month_levels, label="End Month", widget=forms.Select(attrs={'onchange': 'start_date_form.submit();'}))
	end_year = forms.ChoiceField(required=True, choices=year_levels, label="End Year", widget=forms.Select(attrs={'onchange': 'start_date_form.submit();'}))