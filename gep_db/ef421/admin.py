#ef421 admin.py
from django.contrib import admin
from django import forms
from ef421.models import *
from loz_lol.models import Part
from django.db.models import F

# Register your models here.
if 'delete_selected' in admin.site.actions:
    admin.site.disable_action('delete_selected')

def delete_formaPtisis(modeladmin, request, queryset):
	for obj in queryset:
		aircraft = Aircraft.objects.get(pk=obj.aircraft.pk)
		aircraft.ac_flight_hours 	-= obj.flight_hours_today
		aircraft.ac_landings		-= obj.landings_today
		aircraft.save()
		##Update install parts when a flight is erased
		Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True).exclude(part_number='3G2591V01532').\
								update(part_tot_landings=F('part_tot_landings')-obj.landings_today,\
		 								part_tot_flight_hours=F('part_tot_flight_hours')-obj.flight_hours_today)
		##########################################################################################################################################
		##########################################################################################################################################
		#############################################				PENALTIES									##################################
		time_today = obj.flight_hours_today
		Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3G6210A00131').update(part_tot_landings=\
															F('part_tot_landings')-5*obj.start_stop)

		hoist_lift_tot = obj.hoist_lifts_main + obj.hoist_lifts_sec
		Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3G6230A00332').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')-(0.5*hoist_lift_tot))

		if (obj.cargo_cycles > 0):
			Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3G6220A00332').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')-1*obj.cargo_cycles)
			Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3G6330A00532').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')-1*obj.cargo_cycles)
			Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3G6330A00532').update(part_tot_landings=\
															F('part_tot_landings')-2*obj.cargo_cycles)
			Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3T6510V00152').update(part_tot_landings=\
															F('part_tot_landings')-2*obj.cargo_cycles)
			Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3T6521A07353').update(part_tot_landings=\
															F('part_tot_landings')-2*obj.cargo_cycles)
			Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3T6521A05657').update(part_tot_landings=\
															F('part_tot_landings')-2*obj.cargo_cycles)

		if (obj.above_6400 > 0):
			Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3G5510A03931').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')+time_today-4.5*obj.above_6400)
			Part.objects.filter(part_location=aircraft.ac_marks, part_is_installed=True, part_number='3G6420A00332').update(part_tot_flight_hours=\
															F('part_tot_flight_hours')+time_today-1.25*obj.above_6400)

		obj.delete()


class FormaPtisisAdmin(admin.ModelAdmin):
	form = formaPtisisModelForm
	fieldsets = [       (None,               {'fields': ['aircraft', 'flight_hours_today', 'flight_minutes_today', 'landings_today']}),
		('Penalties', {'fields': ['hoist_lifts_main', 'hoist_lifts_sec', 'cat_a', 'start_stop', 'cargo_cycles', 'above_6400']}),
	]
	actions = [delete_formaPtisis,]
	list_filter =('aircraft',)
	list_display = ('aircraft','date', 'display_flight_hours', 'landings_today')

class ItemMoveAdmin(admin.ModelAdmin):
	def part_desc(self, obj):
		return obj.part.part_number.part_description
	list_display = ('date', 'part', 'part_desc', 'move_type', 'comments', 'rel_aircraft')
	search_fields 		= ['comments', 'part__part_serial']

admin.site.register(item_movement, ItemMoveAdmin)
admin.site.register(formaPtisis, FormaPtisisAdmin)


'''
	def has_add_permission(self, request):
		#Disable Add
		return True
    '''
