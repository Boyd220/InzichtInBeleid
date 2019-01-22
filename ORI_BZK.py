import pandas as pd
import numpy as np
import time
import http.client as httplib
"""Set of functions to use in application"""

def get_data():
    try:
        events = pd.read_json('total_dh.json', orient='records')
    except:
        events = pd.read_json('total.json', orient='records')
    return(events)


def count_words(wordslist, sourcedict, countfield):
    temp = pd.Series(np.zeros((len(sourcedict[countfield]))))
    for term in wordslist:
        temp += sourcedict[countfield].str.count(term)
    return temp


def get_searchmatrix(searchword):
    if searchword == 'gas':
        searchterms = ['gaslo', 'gasvrij', 'nul op de meter', 'energieneutraal', 'energietransitie']
    elif searchword == 'wonen':
        searchterms = ['woon', 'wonen', 'woning', 'huis', 'appartement']
    else:
        searchterms = [searchword]
    return searchterms


def get_selection(events, searchword):
    tm = time.time()
    searchterms = get_searchmatrix(searchword)
    #events = get_data()
    events['count'] = count_words(wordslist=searchterms, sourcedict=events, countfield='document')
    events['count_summary'] = count_words(wordslist=searchterms, sourcedict=events, countfield='summary')
    events = events.sort_values(by=['count_summary', 'count'], ascending=False)
    results = events[(events['count'] > 0) | (events['count_summary'] > 0)]
    print(time.time()-tm)
    return(results)


def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=1)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False
