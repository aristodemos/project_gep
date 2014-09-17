#ef421 admin.py
from django.contrib import admin
from django import forms
from ef421.models import *
from loz_lol.models import Part

# Register your models here.

admin.site.register(remove_item)
admin.site.register(install_item)