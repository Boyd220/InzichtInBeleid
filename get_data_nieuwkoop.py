import requests
import json
import pickle

base = 'http://api.openraadsinformatie.nl/v0/search/events'
query = {"query": "",
         "filters": {"organization_id": {
             "terms": ["gemeente-nieuwkoop-nieuwkoop"]}},
         "size": "10",
         "scroll": "5m"}
r = requests.post(base, data=json.dumps(query))
events = r.json()["events"]
print(len(events))
total = r.json()["meta"]["total"]

while len(events) < total:
    # query["scroll_id"] = r.json()["meta"]["scroll"]
    r = requests.post(base, data=json.dumps({"scroll_id": r.json()["meta"]["scroll"], "scroll": "1m"}))
    if "events" not in r.json():
        break
    events += r.json()["events"]
    print(len(events))

data={}
i=0
for event in events:
    if 'sources' in ori_events[i]:
        for source in event['sources']:
            data[source['url']]={'document':source['description'],
                           'summary':source['note'],
                           'masterID':event['id'],
                           'place':event['organization']['id'],
                           'date':event['start_date'],
                           'author':'unknown'}
        i+=1
        if i>10:
            break


try:
    with open("C:/Users/Kraan/Git/ORI/ori.json", "wb") as f:
        json.dump(data, f)      
    with open("C:/Users/Kraan/Git/ORI/nieuwkoop", "wb") as f:
        pickle.dump(events, f)
except:
    with open("C:/Users/Jaap/Git/ORI/ori.json", "w") as f:
        json.dump(data, f)      
    with open("C:/Users/Jaap/Git/ORI/nieuwkoop", "wb") as f:
        pickle.dump(events, f)
    
