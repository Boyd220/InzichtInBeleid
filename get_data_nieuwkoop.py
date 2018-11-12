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

print(len(events))
with open("C:/Users/Kraan/Git/ORI/nieuwkoop", "wb") as f:
    pickle.dump(events, f)
