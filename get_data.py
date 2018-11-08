import requests
import pandas as pd
import json
import pickle

base = 'http://api.openraadsinformatie.nl/v0/search/events'

query = {"query": "",
         "filters": {"start_date": {
             "from": "2018-10-29",
             "to": "2018-11-08"}},
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
with open("save.p", "wb") as f:
    pickle.dump(events, f)


