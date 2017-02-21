# -*- coding: utf-8 -*-
import xlrd
file = xlrd.open_workbook('test.xls',formatting_info=True)
sheet = file.sheet_by_index(0)
print (sheet.cell(0,2))
print (sheet.cell(1,2))
for rownum in range(sheet.nrows):
        
	row = sheet.row_values(rownum)
	for c_el in row:
		print (c_el, end=' | ')
	print ("\n")
