import json
import pandas as pd
import numpy as np

try:
    events = pd.read_json('C:/Users/Kraan/Git/ORI/total.json', orient='records')
except:
    events = pd.read_json('C:/Users/Jaap/Git/ORI/total.json', orient='records')

def count_words(wordslist,sourcedict,countfield):
    temp = pd.Series(np.zeros((len(sourcedict[countfield]))))
    for term in wordslist:
        temp+=sourcedict[countfield].str.count(term)
    return temp

searchterms = ['gaslo','gasvrij','nul op de meter','energieneutraal','energietransitie']

events['count'] = count_words(wordslist=searchterms,sourcedict=events,countfield='document')
events['count_summary'] = count_words(wordslist=searchterms,sourcedict=events,countfield='summary')
events=events.sort_values(by=['count_summary', 'count'],ascending=False)









