from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render

from loz_lol.models import Part, PartList
from ef421.models import *



def index(request):
    #return HttpResponse("AW139.")
    all_partnumbers = PartList.objects.order_by('-part_description')
    output = '\n '.join([p.part_description for p in all_partnumbers])
    return HttpResponse(output)

# Create your views here.
def detail(request, part_id):
	output = "You're looking at part %s." % part_id
	p=Part.objects.get(pk=int(part_id))
	output += "Part Number = %s." % p.part_number
	output += "Part Serial =%s." % p.part_serial
	output += "lifetime limit type =%s." % p.part_number.lifetime.values_list('limit_type')
	output += "Part Location =%s." % p.part_location
	output += "Part Total Flight Hours =%s." % p.part_tot_flight_hours
	output += "Part Total Landings =%s." % p.part_tot_landings
	output += "Part Total Life =%s." % p.part_tot_life
	
	output += "Part Last Installation Date =%s." % p.part_last_in_date
	output += "Part Last Removal Date =%s." % p.part_last_rem_date

	return HttpResponse(output)