#$ ./manage.py shell < myscript.py
from loz_lol.models import Part, PartList
import csv, sys


filename = 'sers703_x.csv'
input_data = open(filename, 'rU')

with input_data as f:

	def get_part_number(part_number):
		print part_number
		return PartList.objects.get(pk=part_number)
	reader = csv.reader(f, delimiter=';', quotechar='\r')
	try:
		for row in reader:
		#now for serial numbers
			created = Part.objects.get_or_create(
				part_number				=get_part_number(row[1]),
				part_serial				=row[2],
				part_is_installed		=True,
				part_location			=row[8],
				part_tot_flight_hours	=row[5],
				part_tot_landings		=row[6],
				part_tot_life			=row[4],
				part_position			=row[3],
				part_last_in_date		=row[7],
				#lifetime=row[3]
				)
		#for lifetimes

	except csv.Error as e:
		sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


#filename = 'parts_desc.csv'
#input_data = open(filename, 'rU')
#
#with input_data as f:
#
#	reader = csv.reader(f, delimiter=';', quotechar='\r')
#	try:
#		for row in reader:
#		#for partnumbers
#			created = PartList.objects.get_or_create(
#				part_number=row[0],
#				part_description=row[1],
#				part_ata_chapter=row[2],
#				#lifetime=row[3]
#				)
#	except csv.Error as e:
#		sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
