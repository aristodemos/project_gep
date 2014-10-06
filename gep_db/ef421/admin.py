#ef421 admin.py
from django.contrib import admin
from django import forms
from ef421.models import *
from loz_lol.models import Part
from django.db.models import F

# Register your models here.
def delete_model(modeladmin, request, queryset):
	for obj in queryset:
		aircraft = Aircraft.objects.get(pk=obj.aircraft.pk)
		aircraft.ac_flight_hours 	-= obj.flight_hours_today
		aircraft.ac_landings		-= obj.landings_today
		aircraft.save()
		##Update install parts when a flight is erased
		Part.objects.filter(part_location=aircraft.ac_marks).\
								update(part_tot_landings=F('part_tot_landings')-obj.landings_today,\
		 								part_tot_flight_hours=F('part_tot_flight_hours')-obj.flight_hours_today)
		####################
		'''
		#SPECIAL CASE FOR PARTS THAT TAKE PENALTIES
		penalties_today = []
		penalties_today.append(obj.hoist_lifts_main)
		penalties_today.append(obj.hoist_lifts_sec)
		penalties_today.append(obj.cat_a)
		penalties_today.append(obj.start_stop)
		penalties_today.append(obj.cargo_cycles)
		penalties_today.append(obj.above_6400)
		'''
		obj.delete()


class FormaPtisisAdmin(admin.ModelAdmin):
	form = formaPtisisModelForm
	def get_actions(self, request):
		#Disable delete
		actions = super(FormaPtisisAdmin, self).get_actions(request)
		del actions['delete_selected']
		return actions

	fieldsets = [       (None,               {'fields': ['aircraft', 'flight_hours_today', 'flight_minutes_today', 'landings_today']}),
		('Penalties', {'fields': ['hoist_lifts_main', 'hoist_lifts_sec', 'cat_a', 'start_stop', 'cargo_cycles', 'above_6400']}),
	]
	actions = [delete_model]
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
