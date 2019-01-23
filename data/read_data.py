# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 14:27:07 2019

@author: Kraan
"""
from pattern.nl import sentiment
from openpyxl import load_workbook
from collections import Counter

stack='C:/Users/Kraan/stack/'
sourcelocation=stack+'DATA/KETENINFORMATIE/Bronckhorst/'
sources=[['teksten op de fotos bronckhorst energierallys.xlsx','tekst'],
         ["Bezetting + aanmelding Energierally's.xlsx",'open vragen'],
         ['13011_Dataset onderzoek Duurzaamheid.xlsx','enquette']]

print(sentiment('Een onwijs spannend goed boek!'))



def countrows(ws,colnum=1,rownum=1):
    column=colnum
    row=rownum
    value = ws.cell(row=row,column=column).value
    while value != '' and value is not None:
        row += 1
        value = ws.cell(row=row,column=column).value
    return(row-1)

def countcols(ws,colnum=1,rownum=1):
    column=colnum
    row=rownum
    value = ws.cell(row=row,column=column).value
    while value != '' and value is not None:
        column += 1
        value = ws.cell(row=row,column=column).value
    return(column-1)
    
totalresult=[]
for source in sources:
    sourcefile=source[0]
    wb = load_workbook(filename = sourcelocation+sourcefile)
    if 'dataprep' in wb.sheetnames:
        ws=wb['dataprep']
    else:
        ws=wb.active
    
    if source[1]=='enquette':
        rows=countrows(ws=ws,colnum=1,rownum=4)
    columns=countcols(ws=ws,colnum=1,rownum=1)

    if source[1]=='enquette':
        result=[]
        for col in range(2,columns):
            question=ws.cell(row=2,column=col).value
            questype=ws.cell(row=3,column=col).value
            subresult=[]
            for row in range(4,rows):
                cellvalue=ws.cell(row=row,column=col).value
                if questype=='open' and (cellvalue==0 or cellvalue is None):
                    cellvalue=''
                else:
                    subresult.append(cellvalue)
            if questype=='meerkeuze':
                subresult=Counter(subresult)
            subresult=[question,questype,subresult,col-1]
            result.append(subresult)
            
    elif source[1]=='open vragen':
        result=[]
        for row in range(2,rows):
            question=ws.cell(row=row,column=1).value
            questype='open'
            subresult=[]
            for col in range(4,columns):
                cellvalue=ws.cell(row=row,column=col).value
                if cellvalue is not None:
                    subresult.append(cellvalue)
            subresult=[question,questype,subresult,row-1]
            result.append(subresult)
            
    elif source[1]=='tekst':
        result=[]
        for row in range(2,rows):
            question=ws.cell(row=row,column=1).value
            questype='open'
            subresult=[question]
            subresult=[question,questype,subresult,row-1]
            result.append(subresult)
    
    for row in result:
        totalresult.append(['inwoner', '1-1-2019', row[2], sourcefile+'_'+str(row[3]), sourcefile, 'Brockhorst', row[0], source[1], row[1]])







['author', 'date', 'document', 'id', 'masterID', 'place', 'summary', 'type', 'open/gesloten']
['author', 1-1-17, 'document', 'id', 'mid', 'Brockhorst', 'summary', 'raad', 'open']
['bewoner', 1-1-19, [antwoord], 'id', 'mid', 'Brockhorst', vraag, 'enquette', 'open']
['bewoner', 1-1-19, [keuze, aantal], 'id', 'mid', 'Brockhorst', vraag, 'enquette', 'gesloten']
['bewoner', 1-1-19, [antwoord], 'id', 'mid', 'Brockhorst', vraag, 'tafelgesprek', 'open']
['bewoner', 1-1-19, [tekst], 'id', 'mid', 'Brockhorst', '', 'fototeksten', 'open']





















try:
    import httplib
except:
    import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False







