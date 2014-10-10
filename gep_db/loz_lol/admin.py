#/home/pafi/.virtualenvs/test_gep_db/lib/python2.7/site-packages/django/contrib/admin/templates/admin/
from django.contrib import admin
import datetime as dd
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core.context_processors import csrf


#from loz_lol.models import Aircraft, PartList, Lifetime_Limit
from loz_lol.models import *
from ef421.models import item_movement

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
admin.site.disable_action('delete_selected')

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
		PART_POSITION_CHOICES = (('0', 'n/a'), ('1', 'Left'),('2', 'Right'), ('3', 'Hoist'), ('4', 'Main'), ('5', 'Secondary'))
		_selected_action 	= forms.CharField(widget=forms.MultipleHiddenInput)
		aircraft 			= forms.ModelChoiceField(Aircraft.objects, empty_label='None aircraft selected')
		part_source			= forms.CharField(max_length=100)

	class RemoveItemsForm(forms.Form):
		_selected_action 	= forms.CharField(widget=forms.MultipleHiddenInput)
		reason_of_removal	= forms.CharField(max_length=100)

	def Remove_Items(self, request, queryset):
		form = None
		if 'apply' in request.POST:
			form = self.RemoveItemsForm(request.POST)
			if form.is_valid():
				comment_frm = form.cleaned_data['reason_of_removal']
				count = 0
				total_items_in_queryset = len(queryset)
				for part in queryset:
					if part.part_is_installed == False:
						continue
					aircraft = Aircraft.objects.get(ac_marks=part.part_location)
					part.part_is_installed = False
					part.part_location = "Store"
					part.part_last_rem_date = datetime.today()
					part.save()
					##the following 3 lines are not necessary - parts' hours are updated after every formaPtisis entry
					'''
					last_in = item_movement.objects.filter(part=part, move_type='RM').latest('date')
					part.part_tot_flight_hours = part.part_tot_flight_hours + aircraft.ac_flight_hours - last_in.rel_ac_hours
					part.part_tot_landings = part.part_tot_landings + aircraft.ac_landings - last_in.rel_ac_landings
					'''
					###################
					#insert Removal Record
					removed_part = item_movement(move_type='RM', rel_aircraft=aircraft, part=part, rel_ac_hours=aircraft.ac_flight_hours, rel_ac_landings=aircraft.ac_landings, comments = "reason of removal: "+comment_frm)
					removed_part.save()
					count += 1
				self.message_user(request, "Successfully removed %d parts from Aircraft." % (count))
				if count != total_items_in_queryset:
					self.message_user(request, "%d were not removed because they ARE NOT installed." % (total_items_in_queryset-count))
				return HttpResponseRedirect(request.get_full_path())
		if not form:
			form = self.RemoveItemsForm(initial={'_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

		return render_to_response('admin/multi_removal_form.html', {'parts':queryset, 'removal_form': form,}, context_instance=RequestContext(request))



	def Install_Items(self, request, queryset):
		form = None
		if 'apply' in request.POST:
			form = self.InstallItemsForm(request.POST)
			#form = PartForm(request.Post)
			if form.is_valid():
				aircraft 	= form.cleaned_data['aircraft']
				comment_frm = form.cleaned_data['part_source']
				count = 0
				total_items_in_queryset = len(queryset)
				for part in queryset:
					if part.part_is_installed == True:
						continue
					part.part_is_installed = True
					part.part_location = aircraft.ac_marks
					part.part_last_in_date = datetime.today()
					part.save()
					###################
					#Update Part Total Hours & Landings
					###################
					installed_part = item_movement(move_type='IN', rel_aircraft=aircraft, part=part, rel_ac_hours=aircraft.ac_flight_hours, rel_ac_landings=aircraft.ac_landings, comments = "part source: "+comment_frm)
					installed_part.save()
					count += 1
				self.message_user(request, "Successfully added %d parts to Aircraft." % (count))
				if count != total_items_in_queryset:
					self.message_user(request, "%d were not installed because they ARE already installed." % (total_items_in_queryset-count))
				return HttpResponseRedirect(request.get_full_path())

		if not form:
			form = self.InstallItemsForm(initial={'_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
			#form = PartForm(initial={'_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

		return render_to_response('admin/multi_installation_form.html', {'parts':queryset, 'installation_form': form,}, context_instance=RequestContext(request))
		#return render(request, 'admin/multi_installation_form.html', {'parts':queryset, 'installation_form': form,})

	list_display = ('part_description', 'part_number', 'part_serial', 'part_location', 'part_remaining_life', 'lifetime', 'expiry_date')
	list_filter =('part_location',)
	search_fields = ['part_number__part_number', 'part_number__part_description',]
	actions = ['Remove_Items', 'Install_Items']

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
	list_display = ('ac_marks', 'display_flight_hours', 'ac_landings', 'ac_flight_hours', 'ac_sn', 'ac_type')


# Register your models here.
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(PartList, PartListAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Lifetime_Limit, LifetimeAdmin)
