#/home/pafi/.virtualenvs/test_gep_db/lib/python2.7/site-packages/django/contrib/admin/templates/admin/
from django.contrib import admin
import datetime as dd
from django import forms
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf


#from loz_lol.models import Aircraft, PartList, Lifetime_Limit
from loz_lol.models import *

class PartInline(admin.TabularInline):
	model = Part
	#list_display = ('part_number', 'part_serial')

class LifeInline(admin.TabularInline):
	model = Part_Life
	readonly_fields = ['limit_type', 'limit_desc']
	
	def limit_type(self, instance):
		return instance.lifetime.limit_type

	def limit_desc(self, instance):
		return instance.lifetime.lifetime_desc()
	
	limit_type.short_description = 'Limit Type'
	limit_desc.short_description = 'Years'

#Adding actions to PartAdmin Model


def Remove_Items(modeladmin, request, queryset):
	#queryset.update(part_location='Store', part_is_installed=False, part_last_rem_date=datetime.today(), part_position="n/a")
	for obj in queryset:
		obj.part_location='Store'
		obj.part_is_installed=False
		obj.part_last_rem_date=datetime.today()
		obj.part_position="n/a"
		obj.save()

	Remove_Items.short_description = 'Remove selected parts from Aircraft'

class PartAdmin(admin.ModelAdmin):
	def part_description(self, obj):
		return obj.part_number.part_description
	
	def lifetime(self, obj):
		out = ''
		for i in obj.part_number.lifetime.values_list('limit_type'):
			 out += " "+str(i)[3:5]
		#return obj.part_number.lifetime.values_list('limit_type')
		return out

	def expiry_date(self, obj):
		part_lifes = Part_Life.objects.filter(part_number=obj.part_number)
		days_to_live = []
		for life in part_lifes:
			days_to_live.append(life.lifetime.limit_calendar_years*365 + life.lifetime.limit_calendar_months*30 + life.lifetime.limit_calendar_days- obj.part_tot_life)
		if len(days_to_live) > 0:
			today = dd.date.today()
			return today + timedelta(min(days_to_live))
		else:
			return ''
	
	class InstallItemsForm(forms.Form):
		_selected_action 	= forms.CharField(widget=forms.MultipleHiddenInput)
		aircraft 			= forms.ModelChoiceField(Aircraft.objects, empty_label='None aircraft selected')
	
	def Install_Items(self, request, queryset):
		form = None
		if 'apply' in request.POST:
			form = self.InstallItemsForm(request.POST)
			if form.is_valid():
				aircraft = form.cleaned_data['aircraft']
				count = 0
				for part in queryset:
					part.part_is_installed = True
					part.part_location = aircraft.ac_marks
					part.part_last_in_date = datetime.today()
					part.save()
					count += 1
				self.message_user(request, "Successfully added %d parts to Aircraft." % (count))
				return HttpResponseRedirect(request.get_full_path())
	
		if not form:
			form = self.InstallItemsForm(initial={'_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
	
		return render_to_response('admin/multi_installation_form.html', {'parts':queryset, 'installation_form': form,}, context_instance=RequestContext(request))


	list_display = ('part_description', 'part_number', 'part_serial', 'part_location', 'part_remaining_life', 'lifetime', 'expiry_date')
	list_filter =('part_location',)
	search_fields = ['part_number__part_number', 'part_number__part_description',]
	actions = [Remove_Items, Install_Items]
	
class PartListAdmin(admin.ModelAdmin):
	def lifetime_it(self, obj):
		out = ''
		for i in obj.lifetime.values_list('limit_type'):
			 out += " "+str(i)[3:5]
		return out

		#_meta

	list_display 		= ('part_description', 'part_number', 'lifetime_it')
	search_fields 		= ['part_number', 'part_description', ]
	list_filter 		= ('lifetime__limit_type',)
	inlines				=[LifeInline, PartInline]
	
		
class PartsInline(admin.StackedInline):
	model = PartList.lifetime.through
	extra = 4

class LifetimeAdmin(admin.ModelAdmin):
	list_display = ('lifetime_desc',)
	inlines =[PartsInline,]

class AircraftAdmin(admin.ModelAdmin):
	list_display = ('ac_marks', 'ac_flight_hours', 'ac_landings', 'ac_sn', 'ac_type')

# Register your models here.
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(PartList, PartListAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Lifetime_Limit, LifetimeAdmin)