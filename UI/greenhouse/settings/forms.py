from django import forms
from scripts.data_handler import data_handler

stateAbbreviations = [
    'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA',
    'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA',
    'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
    'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
    'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY'
]
stateAbbreviations = list(
    map(lambda i, j: (i, j), stateAbbreviations, stateAbbreviations))


class PlantProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        plant_profile_choices = [("Custom", "Custom")]
        profiles = data_handler.get_available_profiles()
        for profile in profiles:
            plant_profile_choices.append(profile)
        self.fields['plant_profile'].choices = plant_profile_choices

    plant_profile = forms.ChoiceField(required=False, label="Plant Profile", widget=forms.Select(
        attrs={'onchange': 'plant_profile_form.submit();'}))


class HealthyLevelsForm(forms.Form):
    temperature_choices = data_handler.get_available_temperatures()
    humidity_choices = data_handler.get_available_humidities()
    sunlight_choices = data_handler.get_available_sunlights()
    soil_moisture_static_choices = data_handler.get_available_soil_moisture_statics()
    soil_moisture_wet_choices = data_handler.get_available_soil_moisture_wets()
    soil_moisture_dry_choices = data_handler.get_available_soil_moisture_drys()
    days_choices = data_handler.get_available_days()
    run_choices = data_handler.get_available_runs()

    temperature = forms.ChoiceField(required=False, choices=temperature_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    humidity = forms.ChoiceField(required=False, choices=humidity_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    sunlight = forms.ChoiceField(required=False, choices=sunlight_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    soil_moisture_static = forms.ChoiceField(required=False, label="Soil Moisture Static", choices=soil_moisture_static_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    soil_moisture_wet = forms.ChoiceField(required=False, label="Soil Moisture Wet", choices=soil_moisture_wet_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    soil_moisture_dry = forms.ChoiceField(required=False, label="Soil Moisture Dry", choices=soil_moisture_dry_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    days = forms.ChoiceField(required=False, label="Water Every", choices=days_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    run = forms.ChoiceField(required=False, label="Run Dynamic Soil Goal", choices=run_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))


class SaveProfileForm(forms.Form):
    temperature_choices = data_handler.get_available_temperatures()
    humidity_choices = data_handler.get_available_humidities()
    sunlight_choices = data_handler.get_available_sunlights()
    soil_moisture_static_choices = data_handler.get_available_soil_moisture_statics()
    soil_moisture_wet_choices = data_handler.get_available_soil_moisture_wets()
    soil_moisture_dry_choices = data_handler.get_available_soil_moisture_drys()
    days_choices = data_handler.get_available_days()
    run_choices = data_handler.get_available_runs()

    custom_temperature = forms.ChoiceField(required=False, choices=temperature_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    custom_humidity = forms.ChoiceField(required=False, choices=humidity_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    custom_sunlight = forms.ChoiceField(required=False, choices=sunlight_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    custom_soil_moisture_static = forms.ChoiceField(required=False, label="Soil Moisture Static", choices=soil_moisture_static_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    custom_soil_moisture_wet = forms.ChoiceField(required=False, label="Soil Moisture Wet", choices=soil_moisture_wet_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    custom_soil_moisture_dry = forms.ChoiceField(required=False, label="Soil Moisture Dry", choices=soil_moisture_dry_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    custom_days = forms.ChoiceField(required=False, label="Water Every", choices=days_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    custom_run = forms.ChoiceField(required=False, label="Run Dynamic Soil Goal", choices=run_choices, widget=forms.Select(
        attrs={'onchange': 'healthy_levels_form.submit();'}))
    profile_name = forms.CharField(max_length=100, label="Profile Name")


class ModeForm(forms.Form):
    mode = forms.ChoiceField(required=False, choices=[('machine_learning', 'Machine Learning'), (
        'manual', 'Manual')], widget=forms.Select(attrs={'onchange': 'mode_form.submit();'}))


class ActionForm(forms.Form):
    actions = [('off', '0 sec repeat'), ('low', '30 sec repeat'),
               ('high', '60 sec repeat')]
    water = forms.ChoiceField(required=True, choices=actions, label="Water", widget=forms.Select(
        attrs={'onchange': 'action_form.submit();'}))
    fan = forms.ChoiceField(required=True, choices=actions, label="Fan", widget=forms.Select(
        attrs={'onchange': 'action_form.submit();'}))
    heat = forms.ChoiceField(required=True, choices=actions, label="Heat", widget=forms.Select(
        attrs={'onchange': 'action_form.submit();'}))
    light = forms.ChoiceField(required=True, choices=actions, label="Light", widget=forms.Select(
        attrs={'onchange': 'action_form.submit();'}))


class AlertForm(forms.Form):
    detail_levels = [('high', 'High Detail'), ('low', 'Low Detail')]
    rate_levels = [('day', "Daily"), ('hour', 'Hourly'),
                   ('minute', "Minutely")]
    detail = forms.ChoiceField(required=True, choices=detail_levels, label="Detail",
                               widget=forms.Select(attrs={'onchange': 'alert_form.submit();'}))
    rate = forms.ChoiceField(required=True, choices=rate_levels, label="Rate",
                             widget=forms.Select(attrs={'onchange': 'alert_form.submit();'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'onchange': 'alert_form.submit();'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(
        render_value=True, attrs={'onchange': 'alert_form.submit();'}))


class PwmForm(forms.Form):
    dc_levels = [(str(i), str(i) + ' %') for i in range(0, 101, 10)]
    fan_dc = forms.ChoiceField(required=True, choices=dc_levels, label="Fan Duty Cycles",
                               widget=forms.Select(attrs={'onchange': 'pwm_form.submit();'}))
    light_dc = forms.ChoiceField(required=True, choices=dc_levels, label="Light Duty Cycles",
                                 widget=forms.Select(attrs={'onchange': 'pwm_form.submit();'}))


class FreqForm(forms.Form):
    freq_levels = [(str(i), str(i) + " Hz") for i in range(0, 501, 25)]
    fan_freq = forms.ChoiceField(required=True, choices=freq_levels, label="Fan Frequency",
                                 widget=forms.Select(attrs={'onchange': 'freq_form.submit();'}))
    light_freq = forms.ChoiceField(required=True, choices=freq_levels, label="Light Frequency",
                                   widget=forms.Select(attrs={'onchange': 'freq_form.submit();'}))


class UpdateIntervalForm(forms.Form):
    interval_levels = [('60', '1 Minute'),
                       ('120', '2 Minutes'), ('300', '5 Minutes')]
    interval = forms.ChoiceField(required=True, choices=interval_levels, label="Interval Update Period",
                                 widget=forms.Select(attrs={'onchange': 'update_interval.submit();'}))


class DeleteForm(forms.Form):
    delete_levels = [('no', 'No'), ('yes', 'Yes')]
    delete_field = forms.ChoiceField(required=True, choices=delete_levels, label="Delete Data", widget=forms.Select(
        attrs={'onchange': 'delete_form.submit();'}))


class StartDateForm(forms.Form):
    day_levels = [(('0' + str(i), '0' + str(i)) if i <
                   10 else (str(i), str(i))) for i in range(1, 32)]
    month_levels = [(('0' + str(i), '0' + str(i)) if i <
                     10 else (str(i), str(i))) for i in range(1, 13)]
    year_levels = [(str(i), str(i)) for i in range(2020, 2101)]
    start_day = forms.ChoiceField(required=True, choices=day_levels, label="Start Day", widget=forms.Select(
        attrs={'onchange': 'start_date_form.submit();'}))
    start_month = forms.ChoiceField(required=True, choices=month_levels, label="Start Month", widget=forms.Select(
        attrs={'onchange': 'start_date_form.submit();'}))
    start_year = forms.ChoiceField(required=True, choices=year_levels, label="Start Year", widget=forms.Select(
        attrs={'onchange': 'start_date_form.submit();'}))
    end_day = forms.ChoiceField(required=True, choices=day_levels, label="End Day", widget=forms.Select(
        attrs={'onchange': 'start_date_form.submit();'}))
    end_month = forms.ChoiceField(required=True, choices=month_levels, label="End Month", widget=forms.Select(
        attrs={'onchange': 'start_date_form.submit();'}))
    end_year = forms.ChoiceField(required=True, choices=year_levels, label="End Year", widget=forms.Select(
        attrs={'onchange': 'start_date_form.submit();'}))


class DaysForm(forms.Form):
    day_levels = [(('0' + str(i), '0' + str(i)) if i <
                   10 else (str(i), str(i))) for i in range(0, 61)]
    day = forms.ChoiceField(required=True, choices=day_levels, label="Days Until Germination", widget=forms.Select(
        attrs={'onchange': 'days_form.submit();'}))


class AddressForm(forms.Form):
    street_address = forms.CharField(required=False, max_length=100, label="Street Address", widget=forms.TextInput(
    ))
    city_address = forms.CharField(required=False, max_length=100, label="City", widget=forms.TextInput(
    ))
    state_address = forms.ChoiceField(required=False, label="State", choices=stateAbbreviations, widget=forms.Select(
    ))
    zip_code = forms.CharField(required=False, max_length=5, label="Zip Code", widget=forms.NumberInput(
    ))
    submit_form = forms.ChoiceField(required=True, label="Submit", choices=[('Yes', 'Yes'), ('No', 'No')], widget=forms.Select(
        attrs={'onchange': 'address_form.submit();'}))


class DeleteAddressForm(forms.Form):
    del_addr = forms.CharField(required=True, max_length=5, label="Index of Address to Delete", widget=forms.NumberInput(
    ))
    submit_addr = forms.ChoiceField(required=True, label="Submit", choices=[('Click to Delete', 'Click to Delete')], widget=forms.Select(
        attrs={'onclick': 'delete_address_form.submit(); document.reload();'}))


class TempForm(forms.Form):
    temp = forms.ChoiceField(required=True, label="Temperature Scale", choices=[('Fahrenheit', 'Fahrenheit'), ('Celsius', 'Celsius')], widget=forms.Select(
        attrs={'onchange': 'temp_form.submit();'}))
