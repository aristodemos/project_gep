from django.contrib import admin
from ef421.models import *

# Register your models here.
class RemoveAdmin(admin.ModelAdmin):
	readonly_fields = ('part_data',)

	def part_data(self, obj):
		return obj.part.part_description


admin.site.register(remove_item, RemoveAdmin)
admin.site.register(install_item)