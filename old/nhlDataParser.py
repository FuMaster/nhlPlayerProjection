import xlrd

workbook = xlrd.open_workbook('NHL2011-12.xls')
worksheet = workbook.sheet_by_index(0)
#9,103-106
#9, 131-134
#1-2, 127-130
#print worksheet.row(0)[3].value


for i in range(worksheet.nrows):
	row = worksheet.row(i)
	print "Player: %s %s, CORSI Rel QoC: %s, CORSI QoC: %s, " \
			"CORSI Rel QoT: %s, CORSI QoT: %s" \
			%(row[3].value, row[2].value, row[127].value, row[128].value, row[129].value, row[130].value)



'''
Notes
scope: any NHL player under age of 24 with at least 3 seasons of data
The most popular of such statistics is Corsi, which counts the number
of events that are goals, shots on goal, missed shots, or blocked shots. Fenwick is another
statistic; it is Corsi but without counting blocked shots.

QoC	Quality of Competition - Average Corsi of one's opponents
QoT	Quality of Temmates - Average Corsi of one's teammates
RQoC	Quality of Competition Relative to teammates
RQoT	Quality of Teammates Relative to other teammates

'''