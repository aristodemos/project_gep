#ef421 models.py
from django.db import models
from loz_lol.models import Part, PartList, Part_Life, Lifetime_Limit, Aircraft
from django import forms
# Create your models here.

class remove_item(models.Model):
	from_aircraft		= models.ForeignKey(Aircraft)
	#################################################
	from_ac_hours		= models.FloatField()
	from_ac_landings	= models.PositiveIntegerField()
	#################################################
	part 				= models.ForeignKey(Part)
	reason_of_removal	= models.CharField(max_length = 100)
	date				= models.DateField(auto_now=False, auto_now_add=False, null = True, blank = True)

class install_item(models.Model):
	to_aircraft		= models.ForeignKey(Aircraft)
	part 			= models.ForeignKey(Part)
	################################################
	to_ac_hours		= models.FloatField()
	to_ac_landings	= models.PositiveIntegerField()
	#part source: MEYP, Aircraft, MAEP
	part_source		= models.CharField(max_length = 5)
	date 			= models.DateField(auto_now=False, auto_now_add=False, null = True, blank = True)

class ekkremousesParatiriseis:
	pass

class formaPtisis(models.Model):
	aircraft 			= models.ForeignKey(Aircraft)
	date 				= models.DateField(auto_now=True, auto_now_add=True, null=True, blank=True)
	#flight hours is a positive integer in minutes
	flight_hours_today	= models.PositiveIntegerField()
	landings_today		= models.PositiveIntegerField()

	#PENALTIES
		#hoist lifts
	hoist_lifts_main	= models.PositiveIntegerField(null = True, blank = True)
	hoist_lifts_sec		= models.PositiveIntegerField(null = True, blank = True)
		#start_stop wind < 17 knots
	start_stop			= models.PositiveIntegerField(null = True, blank = True)
		#above 6400Kg take off weight
	above_6400			= models.PositiveIntegerField(null = True, blank = True)
		#cat_a
	cat_a				= models.PositiveIntegerField(null = True, blank = True)
		#cargo_cycles
	cargo_cycles		= models.PositiveIntegerField(null = True, blank = True)

	def save(self, *args, **kwargs):
		aircraft = Aircraft.objects.get(pk=self.aircraft.pk)
		aircraft.ac_flight_hours 	+= self.flight_hours_today
		aircraft.ac_landings		+= self.landings_today
		aircraft.save()
		super(formaPtisis, self).save(*args, **kwargs)


	def __str__(self):              # __unicode__ on Python 2
		return str(self.aircraft) + " "+str(self.date)

class formaPtisisModelForm(forms.ModelForm):
	test = forms.IntegerField()
	class Meta:
		model = formaPtisis
		fields = [ 'flight_hours_today', 'landings_today', 'test']
	def save(self, commit=True):
		test = self.cleaned_data.get('test', None)
		self.instance.flight_hours_today = self.instance.flight_hours_today*60 + test
		return super(formaPtisisModelForm, self).save(commit=commit)
