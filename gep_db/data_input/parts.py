#$ ./manage.py shell < myscript.py
from loz_lol.models import PartList
import csv, sys
filename = 'parts_desc.csv'
input_data = open(filename, 'rU')

with input_data as f:
	reader = csv.reader(f, delimiter=';', quotechar='\r')
	try:
		for row in reader:
			created = PartList.objects.get_or_create(
				part_number=row[0],
				part_description=row[1],
				part_ata_chapter=row[2],
				#lifetime=row[3]		
				)
	except csv.Error as e:
		sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))