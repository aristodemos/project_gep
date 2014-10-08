from django.db import models
from django import forms
from django.forms import ModelForm
from datetime import datetime, timedelta


# Create your models here.
class Aircraft(models.Model):
	ac_type			= models.CharField(max_length = 10)
	ac_sn			= models.PositiveIntegerField()
	ac_marks		= models.PositiveIntegerField()
	#Flight Hours PositiveInteger in minutes
	ac_flight_hours = models.PositiveIntegerField()
	ac_landings		= models.PositiveIntegerField()

	def __str__(self):              # __unicode__ on Python 2
		return str(self.ac_marks)

	def display_flight_hours(self):
		return str(self.ac_flight_hours/60)+'.'+str(self.ac_flight_hours%60)

class Lifetime_Limit(models.Model):
	DISCARD = 'DS'
	OVERHAUL = 'OH'
	FLIGHTHOURS = 'FH'
	RETIREMENT = 'RT'
	LIFETIME_TYPE_CHOICES = (
		(DISCARD, 'Discard'),
		(OVERHAUL, 'Overhaul'),
		(FLIGHTHOURS, 'Flight Hours'),
		(RETIREMENT, 'Retirement'),
	)
	limit_type				= models.CharField(max_length=2, choices=LIFETIME_TYPE_CHOICES, default=FLIGHTHOURS)
	limit_calendar_years	= models.PositiveIntegerField(default=0)
	limit_calendar_months	= models.PositiveIntegerField(default=0)
	limit_calendar_days		= models.PositiveIntegerField(default=0)
	limit_flight_hours		= models.PositiveIntegerField(default=0)
	limit_landings			= models.PositiveIntegerField(default=0)

	#objects 				= LifetimeManager()
	def lifetime_desc(self):
		descsription_to_return = self.get_limit_type_display()+" "
		if self.limit_flight_hours:
			descsription_to_return += str(self.limit_flight_hours)+"FH "
		else:
			descsription_to_return +="0FH "
		if self.limit_calendar_years:
			descsription_to_return += str(self.limit_calendar_years)+"Y "
		else:
			descsription_to_return +="0Y "
		if self.limit_calendar_months:
			descsription_to_return += str(self.limit_calendar_months)+"M "
		else:
			descsription_to_return +="0M "
		if self.limit_calendar_days:
			descsription_to_return += str(self.limit_calendar_days)+"D "
		else:
			descsription_to_return +="0D "
		if self.limit_landings:
			descsription_to_return += str(self.limit_landings)+"LDS "
		else:
			descsription_to_return +="0LDS"

		#+" "+str(self.limit_calendar_months)+" M"+" "+str(self.limit_calendar_days)+" D")
		return unicode(descsription_to_return)
	def __unicode__(self):
		#return self.get_limit_type_display()
		return self.lifetime_desc()

class PartList(models.Model):
	part_number			= models.CharField(max_length = 15, primary_key = True)
	part_description	= models.CharField(max_length = 30, null=True)
	part_ata_chapter	= models.CharField(max_length = 5, blank=True)
	lifetime			= models.ManyToManyField(Lifetime_Limit, blank=True, through='Part_Life')

	def __unicode__(self):
		#return unicode(self.part_description +" "+ self.part_number)
		return unicode(self.part_number)

class Part_Life(models.Model):
	part_number 	= models.ForeignKey(PartList)
	lifetime 		= models.ForeignKey(Lifetime_Limit)

class Part(models.Model):
	#part_description	= models.CharField(max_length = 30, null=True, blank=True)
	part_number			= models.ForeignKey(PartList)
	part_serial			= models.CharField(max_length = 15, blank=True)


	PART_POSITION_CHOICES = (('1', 'Left'),('2', 'Right'), ('0', 'n/a'), ('3', 'Hoist'), ('4', 'Main'), ('5', 'Secondary'))
	part_position		= models.CharField(max_length=1, choices=PART_POSITION_CHOICES, default='0', blank=True, null=True)

	part_is_installed	= models.BooleanField()


	part_location		= models.CharField(max_length = 5)
	#Flight Hours PositiveInteger in Minutes!
	part_tot_flight_hours	= models.PositiveIntegerField()
	part_tot_landings		= models.PositiveIntegerField()
	#Life in Days
	part_tot_life			= models.PositiveIntegerField()

	# +++++++++++++++++++++++++++++++DateTimeField++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	part_last_in_date		= models.DateTimeField(auto_now=False, auto_now_add=False, null = True, blank = True)#++
	# +++++++++++++++++++++++++++++++DateTimeField++++++++++++++                                             #++
	part_last_rem_date		= models.DateTimeField(auto_now=False, auto_now_add=False, null = True, blank = True)#++
	#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def expected_expiry(self):
		lf 		= self.part_number.lifetime.values_list('limit_calendar_years', 'limit_calendar_months', 'limit_calendar_days')
		lf_type = self.part_number.lifetime.values('limit_type')
		output = ''
		if len(lf_type) > 0:
			if lf[0][0]>0 or lf[0][1]>0 or lf[0][2]>0:
				days_delta = lf[0][0]*365 + lf[0][1]*30 + lf[0][2] - self.part_tot_life
				date_out = datetime.now()+timedelta(days=days_delta)
				output += str(date_out.strftime("%Y/%m/%d"))
		if len(lf_type) > 1:
			if lf[1][0]>0 or lf[1][1]>0 or lf[1][2]>0:
				days_delta = lf[0][0]*365 + lf[0][1]*30 + lf[0][2] - self.part_tot_life
				date_out2 = datetime.now()+timedelta(days=days_delta)
				return str(min(date_out, date_out2).strftime("%Y/%m/%d"))
		else:
			return self.part_rem_fh()

	def part_rem_fh(self):
		lf 		= self.part_number.lifetime.values_list('limit_flight_hours')
		lf_type = self.part_number.lifetime.values('limit_type')
		output = ''
		if len(lf_type) > 0:
			if lf[0][0] > 0:
				remaining_days = (lf[0][0] - int(self.part_tot_flight_hours))/(300.0/365) #300FH in a year
				return str( (datetime.now()+timedelta(days=remaining_days)).strftime("%Y/%m/%d")+"*" )
		else:
			return self.part_rem_lands()

	def part_rem_lands(self):
		pass

	def life_limit_tp(self):
		lf = self.part_number.lifetime.values_list('limit_type')
		if len(lf) > 1:
			return (str(lf[0])[3:5]+" - "+str(lf[1])[3:5])
		if len(lf) > 0:
			return str(lf[0])[3:5]
		else:
			return ''

	def part_remaining_life(self):
		lf = self.part_number.lifetime.values_list('limit_flight_hours', 'limit_landings', 'limit_calendar_years', 'limit_calendar_months', 'limit_calendar_days')
		lf_type = self.part_number.lifetime.values('limit_type')
		output = ''
		if len(lf_type) > 0:

			if lf[0][0] > 0:
				output += "FH: "+ str(lf[0][0] - int(self.part_tot_flight_hours))
			if lf[0][1] > 0:
				output +=" Landings: "+ str(lf[0][1] - self.part_tot_landings)
			if lf[0][2]>0 or lf[0][3]>0 or lf[0][4]>0:
				days_delta = lf[0][2]*365 + lf[0][3]*30 + lf[0][4] - self.part_tot_life
				date_out = datetime.now()+timedelta(days=days_delta)
				output += " Exp. Date: " + str(date_out.strftime("%d/%m/%Y"))
		if len(lf_type) >1:
			if lf[1][2]>0 or lf[1][3]>0 or lf[1][4]>0:
				days_delta = lf[1][2]*365 + lf[1][3]*30 + lf[1][4] - self.part_tot_life
				date_out = datetime.now()+timedelta(days=days_delta)
				output += " Exp. Date: " + str(date_out.strftime("%d/%m/%Y"))

		return output
		#return lf.values('limit_flight_hours')
		#- self.part_tot_flight_hours

	def __unicode__(self):              # __unicode__ on Python 2
		return unicode(self.part_number)+"___"+unicode(self.part_serial)

	def filterOnDescription(self):
		return Part.objects.values('part_description').distinct()

	def display_tot_fh(self):
		return str(self.part_tot_flight_hours/60)+'.'+str(self.part_tot_flight_hours%60)


	#class Meta:
		#unique_together = (('part_number', 'part_serial'),)
		#ordering = ('part_remaining_life',)


#Forms
class PartForm(ModelForm):
	_selected_action 	= forms.CharField(widget=forms.MultipleHiddenInput)
	aircraft 			= forms.ModelChoiceField(Aircraft.objects, empty_label='None aircraft selected')
	part_source			= forms.CharField(max_length=100)
	class Meta:
		model = Part
		exclude = ['part_location']
