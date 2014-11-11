from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext, loader
import datetime, json
from django.core import serializers
from loz_lol.models import Part, PartList
from ef421.models import item_movement



def index(request):
    all_parts = Part.objects.order_by('-part_number')
    output = "<a href='/admin/'>Go to admin dashboard<a/>"
    output += ''.join(["<p><a href='"+str(p.id)+"'>"+p.part_number.part_description+'  '+str(p.part_number)+' '+str(p.part_serial)+"</a></p>" for p in all_parts])
    return HttpResponse(output)

# Create your views here.
def detail_old(request, part_id):
    output = "<h2>You're looking at part %s. </h2>" % part_id
    p=Part.objects.get(pk=int(part_id))
    output += "<p>Part Number = %s.</p>" 		% p.part_number
    output += "<p>Part Serial =%s.</p>" 		% p.part_serial
    output += "<p>Part Description = %s.</p>" 		% p.part_number.part_description
    output += "<p>lifetime limit type =%s.</p>" % p.part_number.lifetime.values_list('limit_type')
    output += "<p>Part Location =%s.</p>" 		% p.part_location
    output += "<p>Part Total Flight Hours =%s.</p>" % p.part_tot_flight_hours
    output += "<p>Part Total Landings =%s.</p>" % p.part_tot_landings
    output += "<p>Part Total Life =%s.</p>" 	% p.part_tot_life

    output += "<p>Part Last Installation Date =%s.</p>" % p.part_last_in_date
    output += "<p>Part Last Removal Date =%s.</p>" % p.part_last_rem_date
    metakiniseis = []
    metakiniseis = item_movement.objects.filter(part=p)
    output += "<h2>Part Historical Record</h2><ol>"
    for entry in metakiniseis:
        output += "<li><p>Part <strong>"+ entry.get_move_type_display() +"</strong> on: "
        if entry.move_type == 'RM':
            output +="<strong>"+ str(entry.date)+ "</strong> ("+entry.comments +") from aircraft: "
        else:
            output +="<strong>"+ str(entry.date)+ "</strong> to aircraft: "
        output +="<strong>"+ str(entry.rel_aircraft.ac_marks)+"</strong>.</p> Aircraft Flight Hours: "
        output += str(entry.rel_ac_hours)+". Aircraft Landings: "
        output += str(entry.rel_ac_landings)+"</li>"
    output +="</ol>"
    output += "<a href='/loz_lol/'>Back to All Parts<a/>"
    return HttpResponse(output)

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body><h1>It is now %s.</h1></body></html>" % now
    return HttpResponse(html)

def detail(request, part_id):
    p = Part.objects.get(pk=int(part_id))
    metakiniseis = []
    metakiniseis = item_movement.objects.filter(part=p)
    data = serializers.serialize("json", item_movement.objects.filter(part=p))
    template = loader.get_template('loz_lol/ef405.html')
    context = RequestContext(request, {
        'part_details': p,
        'moves': metakiniseis,
        'jdata': data,
    })
    return HttpResponse(template.render(context))

def all_parts(request):
    parts = Part.objects.all()
    template = loader.get_template('loz_lol/allparts.html')
    context = RequestContext(request, {
        'all_parts_list':  parts,
    })
    return HttpResponse(template.render(context))
