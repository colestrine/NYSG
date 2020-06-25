from django import forms
from scripts.data_handler import data_handler

class PlantProfileForm(forms.Form):
	plant_profile_choices = [("custom", "Custom"), ("profile_1", "Profile 1"), ("profile_2", "Profile 2"), ("profile_3", "Profile 3")]

	plant_profile = forms.ChoiceField(required=False, choices=plant_profile_choices)

class HealthyLevelsForm(forms.Form):
	temperature_choices = [("65_67", "65-67"), ("68_70", "68-70"), ("71_73", "71-73"), ("74_76", "74-76")]
	humidity_choices = [("40_42", "40-42%"), ("43_45", "43-45%"), ("46_48", "46-48%"), ("49_51", "49-51%")]
	soil_moisture_choices = [("25_27", "25-27%"), ("28_30", "28-30%"), ("31_33", "31-33%"), ("34-36", "34-37%")]
	sunlight_choices = [("80_85", "80-85%"), ("86_91", "86-91%"), ("92_97", "92-97%"), ("98_100", "98-100%")]

	healthy_levels = data_handler.read_healthy_levels()

	temperature = forms.ChoiceField(required=False, choices=temperature_choices)
	humidity = forms.ChoiceField(required=False, choices=humidity_choices)
	soil_moisture = forms.ChoiceField(required=False, label="Soil Moisture", choices=soil_moisture_choices)
	sunlight = forms.ChoiceField(required=False, choices=sunlight_choices)