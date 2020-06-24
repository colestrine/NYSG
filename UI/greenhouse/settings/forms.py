from django import forms

class PlantProfileForm(forms.Form):
	plant_profile_choices = [("custom", "Custom")]

	plant_profile = forms.ChoiceField(required=False, choices=plant_profile_choices)

class HealthyLevelsForm(forms.Form):
	temperature_choices = [("65_67", "65-67"), ("68_70", "68-70"), ("71_73", "71-73"), ("74_76", "74-76")]
	humidity_choices = [("65_67", "65-67"), ("68_70", "68-70"), ("71_73", "71-73"), ("74_76", "74-76")]
	soil_moisture_choices = [("65_67", "65-67"), ("68_70", "68-70"), ("71_73", "71-73"), ("74_76", "74-76")]
	sunlight_choices = [("65_67", "65-67"), ("68_70", "68-70"), ("71_73", "71-73"), ("74_76", "74-76")]

	temperature = forms.ChoiceField(required=False, choices=temperature_choices)
	humidity = forms.ChoiceField(required=False, choices=humidity_choices)
	soil_moisture = forms.ChoiceField(required=False, label="Soil Moisture", choices=soil_moisture_choices)
	sunlight = forms.ChoiceField(required=False, choices=sunlight_choices)