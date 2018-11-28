import pandas as pd
import numpy as np

def get_data():
    try:
        events = pd.read_json('C:/Users/Kraan/Git/ORI/total.json', orient='records')
    except:
        events = pd.read_json('C:/Users/Jaap/Git/ORI/total.json', orient='records')
    return(events)

def count_words(wordslist,sourcedict,countfield):
    temp = pd.Series(np.zeros((len(sourcedict[countfield]))))
    for term in wordslist:
        temp+=sourcedict[countfield].str.count(term)
    return temp

def get_searchmatrix(searchword):
    if searchword=='gas':
        searchterms=['gaslo','gasvrij','nul op de meter','energieneutraal','energietransitie']
    elif searchword=='wonen':
        searchterms=['woon','wonen','woning','huis','appartement']
    return searchterms

def get_selection(searchword):
    searchterms=get_searchmatrix(searchword)
    events=get_data()
    events['count'] = count_words(wordslist=searchterms,sourcedict=events,countfield='document')
    events['count_summary'] = count_words(wordslist=searchterms,sourcedict=events,countfield='summary')
    events=events.sort_values(by=['count_summary', 'count'],ascending=False)
    results=events[(events['count']>0) | (events['count_summary']>0)]
    print(len(results))
    return(results)
