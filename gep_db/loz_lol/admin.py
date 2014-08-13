from django.contrib import admin

from loz_lol.models import Aircraft, Part

class PartAdmin(admin.ModelAdmin):
	list_filter = ('part_description',)
	list_display = ('part_description', 'part_serial', 'part_location')
	'''
	class Meta:
		model = Part
		ordering = ('part_description')
	'''



# Register your models here.
admin.site.register(Aircraft)
admin.site.register(Part, PartAdmin)