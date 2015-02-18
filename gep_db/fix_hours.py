from loz_lol.models import Part, PartList
from django.db.models import F

Part.objects.filter(part_location = '701').update(part_tot_flight_hours=F('part_tot_flight_hours')-1620)

'''
Choices are:
                id,
                item_movement,
                part_is_installed,
                part_last_in_date,
                part_last_rem_date,
                part_location,
                part_number,
                part_position,
                part_serial,
                part_tot_flight_hours,
                part_tot_landings,
                part_tot_life
'''
parts701 = Part.objects.filter(part_location = '701')
for part in parts701:
    print part.part_serial, part.part_number, part.part_number.part_description, part.part_tot_flight_hours
