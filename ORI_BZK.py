import json
import pandas as pd
import numpy as np

try:
    ori_events = pd.read_json('C:/Users/Kraan/Git/ORI/ori.json', orient='records')
except:
    ori_events = pd.read_json('C:/Users/Jaap/Git/ORI/ori.json', orient='records')
try:
    with open ('C:/Users/Kraan/Git/ORI/TKS.json', 'rb') as file:
        tks_events = json.load(file)
except:
    with open ('C:/Users/Jaap/Git/ORI/TKS.json', 'rb') as file:
        tks_events = json.load(file)

def count_words(wordslist,sourcedict,countfield):
    temp = pd.Series(np.zeros((len(sourcedict[countfield]))))
    for term in wordslist:
        temp+=sourcedict[countfield].str.count(term)
    return temp

searchterms = ['gaslo','gasvrij','nul op de meter','energieneutraal','energietransitie']

ori_events['count'] = count_words(wordslist=searchterms,sourcedict=ori_events,countfield='document')












df_ori = pd.DataFrame(columns=['event','doc','score'])

for i in range(len(ori_events)):
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



