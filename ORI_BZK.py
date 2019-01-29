import pandas as pd
import numpy as np
import time
import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=1)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

class ORIDC:
    def __init__(self, mainfile,subfile):
        self.maindata = pd.read_json(mainfile, orient='records')
        self.maindata = self.maindata.loc[self.maindata['date']>='2016-01-01']
        self.adddata = pd.read_json(subfile, orient='records')
        self.mainresult = pd.DataFrame(columns=self.maindata.columns)
        self.mcresult = pd.DataFrame(columns=self.adddata.columns)
        self.searchword = ''

    def printcols(self):
        print(self.maindata.columns)


    def filter(self):
        tm = time.time()
        self.searchmatrix()
        if self.searchword == '' :
            self.mainresult = pd.DataFrame(columns=self.maindata.columns)
            self.mcresult = pd.DataFrame(columns=self.adddata.columns)
        else:
            self.mainresult = pd.DataFrame(self.maindata)
            self.mainresult['count'] = self.count_words(sourcedict=self.maindata, countfield='document')
            self.mainresult = self.mainresult.sort_values(by=['count'], ascending=False)
            self.mainresult = self.mainresult[(self.mainresult['count'] > 0)]
            self.mcresult = pd.DataFrame(self.adddata)
            self.mcresult['count'] = self.count_words(sourcedict=self.mcresult, countfield='summary')
            self.mcresult = self.mcresult.sort_values(by=['count'], ascending=False)
            self.mcresult = self.mcresult[(self.mcresult['count'] > 0)]
        print(time.time()-tm)

    def searchmatrix(self):
        if self.searchword == 'gas':
            self.searchword = ['gaslo', 'gasvrij', 'nul op de meter', 'energieneutraal', 'energietransitie']
        elif self.searchword == 'wonen':
            self.searchword = ['woon', 'wonen', 'woning', 'huis', 'appartement']
        elif self.searchword == '' or self.searchword is None:
            self.searchword = ''
        else:
            self.searchword = [self.searchword]

    def count_words(self, sourcedict, countfield):
        temp = pd.Series(np.zeros((len(sourcedict[countfield]))))
        for term in self.searchword:
            temp += sourcedict[countfield].str.count(term)
        return temp
