from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render

from loz_lol.models import Part, PartList
#from ef421.models import *



def index(request):
    #return HttpResponse("AW139.")    "+str(p.id)+"
    all_parts = Part.objects.order_by('-part_number')
    output = "<a href='/admin/'>Go to admin dashboard<a/>"
    output += ''.join(["<p><a href='"+str(p.id)+"'>"+p.part_number.part_description+"</a></p>" for p in all_parts])
    return HttpResponse(output)

# Create your views here.
def detail(request, part_id):
	output = "<h2>You're looking at part %s. </h2>" % part_id
	p=Part.objects.get(pk=int(part_id))
	output += "<p>Part Number = %s.</p>" 		% p.part_number
	output += "<p>Part Serial =%s.</p>" 		% p.part_serial
	output += "<p>lifetime limit type =%s.</p>" % p.part_number.lifetime.values_list('limit_type')
	output += "<p>Part Location =%s.</p>" 		% p.part_location
	output += "<p>Part Total Flight Hours =%s.</p>" % p.part_tot_flight_hours
	output += "<p>Part Total Landings =%s.</p>" % p.part_tot_landings
	output += "<p>Part Total Life =%s.</p>" 	% p.part_tot_life
	
	output += "<p>Part Last Installation Date =%s.</p>" % p.part_last_in_date
	output += "<p>Part Last Removal Date =%s.</p>" % p.part_last_rem_date
	output += "<a href='/loz_lol/'>Back to All Parts<a/>"
	return HttpResponse(output)