#input_retirements
from loz_lol.models import *
import csv, sys
'''
#For Lifetime Limits
filename = 'retirements.csv'
input_data = open(filename, 'rU')

def main():
	with input_data as f:
		
		def get_part_number(part_number):
			print part_number
			return PartList.objects.get(pk=part_number)
		
		reader = csv.reader(f, delimiter=';', quotechar='\r')
		try:
			for row in reader:
			#now for serial numbers
				created = Lifetime_Limit.objects.get_or_create(
					#part_number				=get_part_number(row[1]),
					limit_type				= row[1],
					limit_calendar_years	= row[2],
					#limit_calendar_months
					#limit_calendar_days
					limit_flight_hours		= row[4],
					limit_landings			= row[5],
					)
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

if __name__=="__main__":
	main()
'''
created = PartList.objects.get_or_create(
			part_number = 'XXX___YYY',
			lifetime 	= Lifetime_Limit.objects.get_or_create(
					limit_type				= 'OH',
					limit_calendar_years	= 2,
					limit_flight_hours		= 666,
				)
	)