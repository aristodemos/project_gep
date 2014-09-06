from django.contrib import admin

#from loz_lol.models import Aircraft, PartList, Lifetime_Limit
from loz_lol.models import *
	
class PartInline(admin.TabularInline):
	model = Part
	#list_display = ('part_number', 'part_serial')

class PartAdmin(admin.ModelAdmin):
	
	def part_description(self, obj):
		return obj.part_number.part_description
	
	def lifetime(self, obj):
		out = ''
		for i in obj.part_number.lifetime.values_list('limit_type'):
			 out += " "+str(i)[3:5]
		#return obj.part_number.lifetime.values_list('limit_type')
		return out

	#read_only_fields= ('part_description',)
	list_display = ('part_description', 'part_number', 'part_serial', 'part_location', 'part_remaining_life', 'lifetime')
	list_filter =('part_location',)
	search_fields = ['part_number__part_number', 'part_number__part_description']

class PartListAdmin(admin.ModelAdmin):
	def lifetime_it(self, obj):
		out = ''
		for i in obj.lifetime.values_list('limit_type'):
			 out += " "+str(i)[3:5]
		return out

		_meta

	list_display 		= ('part_description', 'part_number', 'lifetime_it')
	search_fields 		= ['part_number', 'part_description', ]
	list_filter 		= ('lifetime__limit_type',)
	
		
class PartsInline(admin.StackedInline):
	model = PartList.lifetime.through
	extra = 4

class LifetimeAdmin(admin.ModelAdmin):
	list_display = ('lifetime_desc',)
	inlines =[PartsInline,]

# Register your models here.
admin.site.register(Aircraft)
admin.site.register(PartList, PartListAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Lifetime_Limit, LifetimeAdmin)