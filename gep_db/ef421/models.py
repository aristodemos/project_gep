#ef421 models.py
from django.db import models
from loz_lol.models import Part, PartList, Part_Life, Lifetime_Limit, Aircraft
from django import forms
from django.db.models import F
import re
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
	date				= models.DateTimeField(auto_now_add=True, null = True, blank = True)
	date.editable = True

	class Meta:
		ordering = ['date',]

class formaPtisis(models.Model):
	aircraft 			= models.ForeignKey(Aircraft)
	date 				= models.DateField(auto_now=True, auto_now_add=True, null=True, blank=True)
	date.editable		= True
	#flight hours is a positive integer in minutes
	flight_hours_today	= models.PositiveIntegerField()
	landings_today		= models.PositiveIntegerField()

	#PENALTIES
		#hoist lifts
	hoist_lifts_main	= models.PositiveIntegerField(default = 0)
	hoist_lifts_sec		= models.PositiveIntegerField(default = 0)
		#start_stop wind < 17 knots
	start_stop			= models.PositiveIntegerField(default = 0)
		#above 6400Kg take off weight
	above_6400			= models.PositiveIntegerField(default = 0)
		#cat_a
	cat_a				= models.PositiveIntegerField(default = 0)
		#cargo_cycles
	cargo_cycles		= models.PositiveIntegerField(default = 0)

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
	#flight_minutes_today = forms.IntegerField()
	#new form - join flight hours & minutes test area
	p = re.compile('[0-9]{1,3}[:.][0-5]{1}[0-9]{1}')
	flight_minutes_today = forms.CharField()
	class Meta:
		model = formaPtisis
		fields = [ 'flight_hours_today', 'flight_minutes_today', 'landings_today']
	def clean_flight_minutes_today(self):
		data = self.cleaned_data['flight_minutes_today']
		if not self.p.match(data):
			raise forms.ValidationError("Flight time not in the right format! Use HH:MM or HH.MM")
		# Always return the cleaned data, whether you have changed it or
		# not.
		return self.p.match(data).group()
	def save(self, commit=True):
		ffhh_today = self.cleaned_data.get('flight_minutes_today', None)
		if '.' in ffhh_today:
			fhours_today = int(ffhh_today.split('.', 1)[0])
			fminutes_today = int(ffhh_today.split('.', 1)[1])
		elif ':' in ffhh_today:
			fhours_today = int(ffhh_today.split(':', 1)[0])
			fminutes_today = int(ffhh_today.split(':', 1)[1])
		time_today = fhours_today*60 + fminutes_today
		self.instance.flight_hours_today = time_today
		#############################################################
		#				PENALTIES									#
		Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3G6210A00131').update(part_tot_landings=\
															F('part_tot_landings')+5*self.instance.start_stop)

		hoist_lift_tot = self.instance.hoist_lifts_main + self.instance.hoist_lifts_sec
		Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3G6230A00332').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')+(0.5*hoist_lift_tot))

		if (self.instance.cargo_cycles > 0):
			Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3G6220A00332').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')+1*self.instance.cargo_cycles)
			Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3G6330A00532').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')+1*self.instance.cargo_cycles)
			Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3G6330A00532').update(part_tot_landings=\
															F('part_tot_landings')+2*self.instance.cargo_cycles)
			Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3T6510V00152').update(part_tot_landings=\
															F('part_tot_landings')+2*self.instance.cargo_cycles)
			Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3T6521A07353').update(part_tot_landings=\
															F('part_tot_landings')+2*self.instance.cargo_cycles)
			Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3T6521A05657').update(part_tot_landings=\
															F('part_tot_landings')+2*self.instance.cargo_cycles)

		if (self.instance.above_6400 > 0):
			Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3G5510A03931').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')-time_today+4.5*self.instance.above_6400)
			Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True, part_number='3G6420A00332').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')-time_today+1.25*self.instance.above_6400)

		Part.objects.filter(part_location=self.instance.aircraft, part_is_installed=True).exclude(part_number='3G2591V01532').\
										update(part_tot_landings=F('part_tot_landings')+self.instance.landings_today, \
												part_tot_flight_hours=F('part_tot_flight_hours')+self.instance.flight_hours_today)
		#															#
		#############################################################
		return super(formaPtisisModelForm, self).save(commit=commit)
