#ef421 admin.py
from django.contrib import admin
from django import forms
from ef421.models import *
from loz_lol.models import Part

# Register your models here.
def delete_model(modeladmin, request, queryset):
	for obj in queryset:
		aircraft = Aircraft.objects.get(pk=obj.aircraft.pk)
		aircraft.ac_flight_hours 	-= obj.flight_hours_today
		aircraft.ac_landings		-= obj.landings_today
		aircraft.save()
		obj.delete()


class FormaPtisisAdmin(admin.ModelAdmin):
	form = formaPtisisModelForm
	def get_actions(self, request):
		#Disable delete
		actions = super(FormaPtisisAdmin, self).get_actions(request)
		del actions['delete_selected']
		return actions

	fieldsets = [       (None,               {'fields': ['aircraft', 'flight_hours_today', 'landings_today', 'test']}),
		('Penalties', {'fields': ['hoist_lifts_main', 'hoist_lifts_sec', 'cat_a', 'start_stop', 'cargo_cycles', 'above_6400']}),
	]
	actions = [delete_model]
	list_filter =('aircraft',)
	list_display = ('aircraft','date', 'flight_hours_today', 'landings_today')


admin.site.register(remove_item)
admin.site.register(install_item)
admin.site.register(formaPtisis, FormaPtisisAdmin)


'''
	def has_add_permission(self, request):
		#Disable Add
		return True
    '''
