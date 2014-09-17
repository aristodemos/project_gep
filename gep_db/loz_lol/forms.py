#forms.py
from django import forms
from ef421.models import *
from django.forms.models import inlineformset_factory

class MyForm(forms.Form):
	aircraft 			= forms.CharField()
	flight_time_today	= forms.CharField()
	landings_today		= forms.CharField()

class ContactForm(forms.Form):
	marks 			= forms.CharField()
	flight_hours_today	= forms.CharField()
	landings_today		= forms.CharField()
