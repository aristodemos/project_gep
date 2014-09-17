#ef421 models.py
from django.db import models
from loz_lol.models import Part, PartList, Part_Life, Lifetime_Limit, Aircraft
# Create your models here.

class remove_item(models.Model):
	from_aircraft		= models.ForeignKey(Aircraft)
	part 				= models.ForeignKey(Part)
	reason_of_removal	= models.CharField(max_length = 100)
	date				= models.DateField(auto_now=False, auto_now_add=False, null = True, blank = True)

class install_item(models.Model):
	to_aircraft		= models.ForeignKey(Aircraft)
	part 			= models.ForeignKey(Part)
	#part source: MEYP, Aircraft, MAEP
	part_source		= models.CharField(max_length = 5)
	date 			= models.DateField(auto_now=False, auto_now_add=False, null = True, blank = True)

class ef_405:
	pass

