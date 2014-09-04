from django.shortcuts import render
from django.http import HttpResponse
from loz_lol.models import Part, PartList

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

	return HttpResponse(output)