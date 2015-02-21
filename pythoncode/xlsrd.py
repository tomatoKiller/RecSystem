__author__ = 'wu'
import xlrd
'''
data = xlrd.open_workbook("jiayuanUmark.xlsx")
fp = open("rating.txt","w+")
table = data.sheets()[0]
for j in range(1,table.ncols):
    for i in range(1,table.nrows):
        if((table.cell(i,j).value != "") and (table.cell(i,j).value != " \n")):
            temp = "%s::%s::%s\n" %(table.cell(0,j).value, table.cell(i,0).value, table.cell(i,j).value)
            fp.write(temp)
            print temp


'''
data = xlrd.open_workbook("jiayuanUmark.xlsx")
fp = open("boy2girl.txt","w+")
table = data.sheets()[1]
for j in range(1,table.ncols):
    for i in range(1,table.nrows):
        if((table.cell(i,j).value != "") and (table.cell(i,j).value != " \n")):
            temp = "%s::%s::%s\n" %(table.cell(0,j).value, table.cell(i,0).value, table.cell(i,j).value)
            fp.write(temp)
            #print temp
