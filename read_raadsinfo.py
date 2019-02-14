import sys
import os
sys.path.insert(1, 'E:\\PYTHON\\LIB')
from tekkst.readdoc import ExtractInfoFromDoc
import tqdm
import json
from datetime import datetime
docpath = 'E:/DATA/KETENINFORMATIE/Bronckhorst/Raadsinformatie Charel/Word/'

totalresult = []
filenames=os.listdir(docpath)
for i in tqdm.tqdm(range(len(filenames))):
    filename=filenames[i]
    if filename.find('.docx') == -1:
        print(filename)
    else:
        filedate = filename[6:8]+'-'+filename[4:6]+'-'+filename[:4]
        result = ''
        docinfo=ExtractInfoFromDoc(docpath+filename)
        for line in docinfo:
            result += line[0] + ' ' + line[1] + ' '
        summary = filename[9:filename.find('.docx')]
        totalresult.append({'author': 'Raad Bronckhorst',
            'date': filedate,
            'document': result,
            'id': filename,
            'masterID': filename,
            'place': 'Brockhorst',
            'summary': summary})

print('Part 2')

def replacemonth(string):
    for r in (("januari", "January"),
          ("februari", "February"),
          ("maart", "March"),
          ("april", "April"),
          ("mei", "May"),
          ("juni", "June"),
          ("juli", "July"),
          ("augustus", "August"),
          ("september", "September"),
          ("oktober", "October"),
          ("november", "November"),
          ("december", "December")):
        string = string.replace(*r)
    return string

#import tks data
with open ('TKS.json', 'rb') as file:
    tkv_events = json.load(file)

pb = tqdm.tqdm(total=len(filenames)+len(tkv_events))
#get data in right format
for event in tkv_events:
    if type(event['Bestanden']) == str:
        document=event['Bestanden']
    elif type(event['Bestanden']) == list:
        if len(event['Bestanden'])==1:
            document=event['Bestanden'][0]
        else:
            document=''
            for doc in event['Bestanden']:
                document+=doc
    totalresult.append({'id':event['id'],
                     'document':document,
                     'summary':event['Titel'],
                     'masterID':event['id'],
                     'place':'TK',
                     'date':datetime.date(datetime.strptime(replacemonth(event['Publicatiedatum']), '%d %B %Y')).strftime('%d-%m-%Y'),
                     'author':event['Indiener']})
    pb.update(len(totalresult))
pb.close()

#save data
with open("total.json", "w") as f:
    json.dump(total_data, f)
