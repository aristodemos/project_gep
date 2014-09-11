from django.contrib import admin
from django import forms
from ef421.models import *
from loz_lol.models import Part

class InstallForm(forms.ModelForm):
	class Meta:
		model = install_item
		fields = ['part', ]

		def part_description (self, obj):
			return obj.part.part_description


# Register your models here.
class RemoveAdmin(admin.ModelAdmin):
	readonly_fields = ('part_data',)

	def part_data(self, obj):
		return obj.part.part_description

class InstallAdmin(admin.ModelAdmin):
	
	form = InstallForm


admin.site.register(remove_item, RemoveAdmin)
admin.site.register(install_item, InstallAdmin)