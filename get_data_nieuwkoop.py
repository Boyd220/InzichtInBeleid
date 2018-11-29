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
i=0
for event in events:
    if 'sources' in event:
        for source in event['sources']:
            ori_data.append({'id':source['url'],
                         'document':source['description'],
                         'summary':source['note'],
                         'masterID':event['id'],
                         'place':event['organization']['id'],
                         'date':datetime.date(datetime.strptime(event['start_date'][:19], '%Y-%m-%dT%H:%M:%S')).strftime('%d-%m-%Y'),
                         'author':'unknown'})
        i+=1
        if i>10:
            break


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
with open ('C:/Users/Jaap/git/ORI/TKS.json', 'rb') as file:
    tkv_events = json.load(file)

#get data in right format
tkv_data=[]
i=0
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
    i+=1
    if i>20:
        break

total_data=[]
total_data.extend(ori_data)
total_data.extend(tkv_data)

#save data
try:
    with open("C:/Users/Kraan/Git/ORI/total.json", "w") as f:
        json.dump(total_data, f)
except:
    with open("C:/Users/Kraan/Git/ORI/total.json", "w") as f:
        json.dump(total_data, f)
