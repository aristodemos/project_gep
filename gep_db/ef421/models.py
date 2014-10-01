#ef421 models.py
from django.db import models
from loz_lol.models import Part, PartList, Part_Life, Lifetime_Limit, Aircraft
from django import forms
from django.db.models import F
# Create your models here.

class item_movement(models.Model):
	REMOVAL = 'RM'
	INSTALLATION = 'IN'
	MOVEMENT_CHOICE = (
		(REMOVAL, 'Removal'),
		(INSTALLATION, 'Installation'),
	)
	move_type			= models.CharField(max_length=2, choices=MOVEMENT_CHOICE, null=False, blank=False)
	rel_aircraft		= models.ForeignKey(Aircraft)
	rel_ac_hours		= models.PositiveIntegerField()
	rel_ac_landings		= models.PositiveIntegerField()
	part 				= models.ForeignKey(Part)
	comments			= models.CharField(max_length = 100)
	date				= models.DateField(auto_now=True, auto_now_add=True, null = True, blank = True)


class formaPtisis(models.Model):
	aircraft 			= models.ForeignKey(Aircraft)
	date 				= models.DateField(auto_now=True, auto_now_add=True, null=True, blank=True)
	#flight hours is a positive integer in minutes
	flight_hours_today	= models.PositiveIntegerField()
	landings_today		= models.PositiveIntegerField()

	#PENALTIES
		#hoist lifts
	hoist_lifts_main	= models.PositiveIntegerField(default = 0, null = True, blank = True)
	hoist_lifts_sec		= models.PositiveIntegerField(default = 0, null = True, blank = True)
		#start_stop wind < 17 knots
	start_stop			= models.PositiveIntegerField(default = 0, null = True, blank = True)
		#above 6400Kg take off weight
	above_6400			= models.PositiveIntegerField(default = 0, null = True, blank = True)
		#cat_a
	cat_a				= models.PositiveIntegerField(default = 0, null = True, blank = True)
		#cargo_cycles
	cargo_cycles		= models.PositiveIntegerField(default = 0, null = True, blank = True)

	def save(self, *args, **kwargs):
		aircraft = Aircraft.objects.get(pk=self.aircraft.pk)
		aircraft.ac_flight_hours 	+= self.flight_hours_today
		aircraft.ac_landings		+= self.landings_today
		aircraft.save()
		super(formaPtisis, self).save(*args, **kwargs)


	def __str__(self):              # __unicode__ on Python 2
		return str(self.aircraft) + " "+str(self.date)

	def display_flight_hours(self):
		return str(self.flight_hours_today/60)+'.'+str(self.flight_hours_today%60)

class formaPtisisModelForm(forms.ModelForm):
	flight_minutes_today = forms.IntegerField()
	class Meta:
		model = formaPtisis
		fields = [ 'flight_hours_today', 'flight_minutes_today', 'landings_today']
	def save(self, commit=True):
		flight_minutes_today = self.cleaned_data.get('flight_minutes_today', None)
		self.instance.flight_hours_today = self.instance.flight_hours_today*60 + flight_minutes_today
		#############################################################
		#				PENALTIES									#
		'''
		if self.instance.start_stop > 0:
			part_mr_blade = Part.objects.filter(part_number='3G6210A00131')
			self.instance.landings_today += 5
		'''
		Part.objects.filter(part_location=self.instance.aircraft).\
										update(part_tot_landings=F('part_tot_landings')+self.instance.landings_today, \
												part_tot_flight_hours=F('part_tot_flight_hours')+self.instance.flight_hours_today)
		#															#
		#############################################################
		return super(formaPtisisModelForm, self).save(commit=commit)
