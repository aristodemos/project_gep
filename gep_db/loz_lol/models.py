from django.db import models
from django.forms import ModelForm

# Create your models here.
class Aircraft(models.Model):
	ac_type			= models.CharField(max_length = 10)
	ac_sn			= models.PositiveIntegerField()
	ac_marks		= models.PositiveIntegerField()
	#Flight Hours format 00:00 or 00.00
	ac_flight_hours = models.CharField(max_length = 8)
	ac_landings		= models.PositiveIntegerField()

	def __str__(self):              # __unicode__ on Python 2
		return str(self.ac_marks)

class LifetimeManager(models.Manager):
	def lifetime_description(self):
		from django.db import connection
		cursor = connection.cursor()
		cursor.execute(
				"""
				SELECT lf.limit_type, lf.limit_calendar_years, lf.limit_flight_hours, lf.limit_landings
				FROM Lifetime_Limit lf, PartList pl
				WHERE lf.id = pl.id
				""")
		result_list = []
		for row in cursor.fetchall():
			print row
			result_list.append(row)
		return result_list

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
	limit_calendar_years	= models.PositiveIntegerField(null = True, blank = True)
	limit_calendar_months	= models.PositiveIntegerField(null = True, blank = True)
	limit_calendar_days		= models.PositiveIntegerField(null = True, blank = True)
	limit_flight_hours		= models.PositiveIntegerField(null = True, blank = True)
	limit_landings			= models.PositiveIntegerField(null = True, blank = True)
	
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
		return self.get_limit_type_display()

class PartList(models.Model):
	part_number			= models.CharField(max_length = 15, primary_key = True)
	part_description	= models.CharField(max_length = 30, null=True)
	part_ata_chapter	= models.CharField(max_length = 5, blank=True)
	lifetime			= models.ManyToManyField(Lifetime_Limit, blank=True, related_name='part_life')

	def __unicode__(self):
		#return unicode(self.part_description +" "+ self.part_number)
		return unicode(self.part_number)
	

class Part(models.Model):
	#part_description	= models.CharField(max_length = 30, null=True, blank=True)
	part_number			= models.ForeignKey(PartList)
	part_serial			= models.CharField(max_length = 15, blank=True)


	PART_POSITION_CHOICES = (('1', 'Left'),('2', 'Right'), ('0', 'n/a'), ('3', 'Hoist'),)
	part_position		= models.CharField(max_length=1, choices=PART_POSITION_CHOICES, default='0', blank=True, null=True)

	part_is_installed	= models.BooleanField()


	part_location		= models.CharField(max_length = 5)
	#Flight Hours format 00:00 or 00.00
	part_tot_flight_hours	= models.CharField(max_length = 8)
	part_tot_landings		= models.PositiveIntegerField()
	#Life in Days
	part_tot_life			= models.PositiveIntegerField()

	part_last_in_date		= models.DateField(auto_now=False, auto_now_add=False, null = True, blank = True)
	part_last_rem_date		= models.DateField(auto_now=False, auto_now_add=False, null = True, blank = True)

	def __unicode__(self):              # __unicode__ on Python 2
		return unicode(self.part_number)

	def filterOnDescription(self):
		return Part.objects.values('part_description').distinct()

	'''
	class Meta:
		unique_together = (('part_number', 'part_serial'),)
		#ordering = ('part_description',)
	'''

#Forms
'''
class AircraftForm(ModelForm):
	pass

class PartForm(ModelForm):
	pass
#We need a formset !!
class LifetimeLimitForm(ModelForm):
	pass
'''