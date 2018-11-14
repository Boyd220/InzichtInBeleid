import requests
import json
import pickle
import pandas as pd

with open ('C:/Users/Kraan/Desktop/ori.json', 'rb') as file:
    ori_events = json.load(file)
with open ('C:/Users/Kraan/Desktop/TKS.json', 'rb') as file:
    tks_events = json.load(file)

df_ori = pd.DataFrame(columns=['event','doc','score'])

searchterms = ['gaslo','gasvrij','nul op de meter','energieneutraal','energietransitie']
for i in range(len(ori_events)):
    classificatie=ori_events[i]["classification"]
    date=ori_events[i]["start_date"]
    #description=events[i]["description"]
    if 'sources' in ori_events[i]:
        for j in range(len(ori_events[i]["sources"])):
            searchtext=ori_events[i]["sources"][j]["description"]
            score = 0
            for term in searchterms:
                score+=searchtext.count(term)
            df_ori=df_ori.append(pd.DataFrame([[i,j,score]],columns=['event','doc','score']),ignore_index=True)

for key in df_ori:
    df_ori[key]=pd.to_numeric(df_ori[key])
df_ori = pd.merge(df_ori, pd.DataFrame(df_ori.groupby('event')['score'].mean()), right_index=True, left_on='event')


df_tks = pd.DataFrame(columns=['event','score'])
for i in range(len(tks_events)):
    score = 0
    if len(tks_events[i]['Bestanden'])>0:
        searchtext=tks_events[i]['Bestanden'][0]
        for term in searchterms:
            score+=searchtext.count(term)
    score+=tks_events[i]['Titel'].count(term)
    df_tks=df_tks.append(pd.DataFrame([[i,score]],columns=['event','score']),ignore_index=True)

for key in df_tks:
    df_tks[key]=pd.to_numeric(df_tks[key])
