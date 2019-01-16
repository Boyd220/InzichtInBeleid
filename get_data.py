import requests
import json
from datetime import datetime

#ORI API variables
base = 'http://api.openraadsinformatie.nl/v0/search/events'
query = {"query": "",
         "filters": {"organization_id": {
             "terms": ["gemeente-nieuwkoop-nieuwkoop"]}},
         "size": "10",
         "scroll": "5m"}
r = requests.post(base, data=json.dumps(query))
events = r.json()["events"]
total = r.json()["meta"]["total"]

#Loop through ORI API
while len(events) < total:
    # query["scroll_id"] = r.json()["meta"]["scroll"]
    r = requests.post(base, data=json.dumps({"scroll_id": r.json()["meta"]["scroll"], "scroll": "1m"}))
    if "events" not in r.json():
        break
    events += r.json()["events"]
    print(len(events))

#Get data in right format
ori_data=[]
for event in events:
    if 'sources' in event:
        masterid=event['id']
        try:place=event['organization']['id']
        except:place=event['meta']['collection']
        try:date=event['start_date']
        except:date=event['meta']['processing_started']
        date=datetime.date(datetime.strptime(date[:19], '%Y-%m-%dT%H:%M:%S')).strftime('%d-%m-%Y')
        author='unknown'
        if event['classification']=='Moties':
            localid=masterid
            document=event['sources'][0]['description']
            try:summary=event['sources'][0]['note']
            except:summary=event['sources'][0]['notes']
            ori_data.append({'id':localid,
                             'document':document,
                             'summary':summary,
                             'masterID':masterid,
                             'place':place,
                             'date':date,
                             'author':author})
        else:
            for source in event['sources']:
                localid=source['url']
                document=source['description']
                try:summary=source['note']
                except:summary=source['notes']
                ori_data.append({'id':localid,
                             'document':document,
                             'summary':summary,
                             'masterID':masterid,
                             'place':place,
                             'date':date,
                             'author':author})

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

#get data in right format
tkv_data=[]
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
    tkv_data.append({'id':event['id'],
                     'document':document,
                     'summary':event['Titel'],
                     'masterID':event['id'],
                     'place':'TK',
                     'date':datetime.date(datetime.strptime(replacemonth(event['Publicatiedatum']), '%d %B %Y')).strftime('%d-%m-%Y'),
                     'author':event['Indiener']})

total_data=[]
total_data.extend(ori_data)
total_data.extend(tkv_data)

#save data
with open("total.json", "w") as f:
    json.dump(total_data, f)
