#read_gep_data.py
import json
import sys
import unicodedata

all_parts = []

def main():
	global parts
	input_file = open(sys.argv[1])
	#in_file = open('awlol.csv')
	in_file=input_file.read()
	for line in in_file:
		part = line.split('\r')
		for column in part:
			part_col = column.split(';')
			all_parts.append(part_col)

	print all_parts

if __name__ == '__main__':
	main()

'''
import sqlite3
conn = sqlite3.connect('db')
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
for row in c.execute('SELECT * FROM loz_lol_aircraft'):
	print row


(1, u'AW139', 31328, 701, u'860:40', 2203)
 
for row in c.execute('SELECT * FROM loz_lol_part'):     
	print row
'''
