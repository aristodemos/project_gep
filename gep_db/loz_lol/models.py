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

class Part(models.Model):
	part_number			= models.CharField(max_length = 15)
	part_serial			= models.CharField(max_length = 15)

	part_ata_chapter	= models.CharFiel(max_length = 5)

	PART_POSITION_CHOICES = (('1', 'Left'),('2', 'Right'), ('0', 'n/a'),)
	part_position		= models.CharField(max_length=1, choices=PART_POSITION_CHOICES, default='0')

	part_is_installed	= models.BooleanField()
	part_location		= 
	#Flight Hours format 00:00 or 00.00
	part_tot_flight_hours	= models.CharField(max_length = 8)
	part_tot_landings		= models.PositiveIntegerField()
	#Life in Days
	part_tot_life			= models.PositiveIntegerField()

	part_last_in_date		= models.DateField(auto_now=False, auto_now_add=False, null = True, blank = True)
	part_last_rem_date		= models.DateField(auto_now=False, auto_now_add=False, null = True, blank = True)

	def part_location_choices():
		return {}

	class Meta:
		unique_together = (('part_number', 'part_serial'),)


#Forms
class AircraftForm(ModelForm):
	pass

class PartForm(ModelForm):
	pass