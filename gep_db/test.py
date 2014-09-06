from loz_lol.models import *
import csv, sys

filename = 'retirements.csv'
input_data = open(filename, 'rU')
print "aaaa"
with input_data as f:
	
	print "bbbbb"
	reader = csv.reader(f, delimiter=';', quotechar='\r')
	try:
		print "ccccc"
		for row in reader:

			p, created_p = PartList.objects.get_or_create(pk=row[1])
			if (created_p):
				print 'True'
				p = PartList(part_description = row[0])
			else:
				print 'False'

			lf, create_lf = Lifetime_Limit.objects.get_or_create(
			limit_type				=row[5],
			limit_calendar_years	=int(row[13].split('Y')[:1][0]),
			limit_calendar_months	=int(row[13].split(' ')[1].split('M')[:1][0]),
			limit_calendar_days		=int(row[13].split(' ')[2].split('D')[:1][0]),
			limit_flight_hours		=int(row[15]),
			limit_landings			=int(row[16])
				)
			p.lifetime.add(lf)
	
	except csv.Error as e:
		sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

print "ddddd66666"