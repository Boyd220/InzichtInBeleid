import pandas as pd
import numpy as np
import time
import http.client as httplib
from wordcloud import WordCloud
import dash_html_components as html
from io import BytesIO
import base64


def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=1)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


def getbrokenstring(inputstr, value=68):
    if len(inputstr) < value:
        return inputstr
    letter = inputstr[value]
    while letter != ' ':
        value -= 1
        letter = inputstr[value]
    return inputstr[:value]+'<br>'+getbrokenstring(inputstr[value:])


def findvalue(dictio, key):
    """Check if given item exists in given dictionary."""
    try:
        a = dictio[key]
    except:
        return 0
    return a


class ORIDC:
    def __init__(self, mainfile, subfile):
        self.maindata = pd.read_json(mainfile, orient='records')
        self.maindata = self.maindata.loc[self.maindata['date'] >= '2016-01-01']
        self.adddata = pd.read_json(subfile, orient='records')
        self.mainresult = pd.DataFrame(columns=self.maindata.columns)
        self.closedquestion = []
        self.openquestion = []
        self.openanswer = []
        self.searchword = ''

    def printcols(self):
        print(self.maindata.columns)

    def filter(self):
        tm = time.time()
        self.searchmatrix()
        if self.searchword == '':
            # reset results
            self.mainresult = pd.DataFrame(columns=self.maindata.columns)
            self.closedquestion = []
            self.openquestion = []
            self.openanswer = []
        else:
            # filter data with searchword in document
            self.mainresult = pd.DataFrame(self.maindata)
            self.mainresult['count'] = self.count_words(sourcedict=self.maindata, countfield='document')
            self.mainresult = self.mainresult.sort_values(by=['count'], ascending=False)
            self.mainresult = self.mainresult[(self.mainresult['count'] > 0)]

            # filter open en closed question if searchword is in question
            tempdf = pd.DataFrame(self.adddata)
            tempdf['count'] = self.count_words(
                sourcedict=tempdf,
                countfield='summary'
            )
            tempdf = tempdf.sort_values(by=['count'], ascending=False)
            tempdf = tempdf[(tempdf['count'] > 0)]
            for index, row in tempdf.iterrows():
                if row['questype'] == 'meerkeuze':
                    self.closedquestion.append({
                        'title': row['summary'],
                        'data': row['document'][0]
                    })
                elif row['questype'] == 'open':
                    self.openquestion.append({
                        'title': row['summary'],
                        'data': row['wordcounter'],
                        'source': row['document']
                    })

            # filter open question if searchword is in answers
            tempdf = pd.DataFrame(self.adddata)
            tempdf['count'] = self.count_words_dicts(
                sourcedict=tempdf,
                countfield='wordcounter'
            )
            tempdf = tempdf.sort_values(by=['count'], ascending=False)
            tempdf = tempdf[(tempdf['count'] > 0)]
            for index, row in tempdf.iterrows():
                if row['questype'] == 'open':
                    self.openanswer.append({
                        'title': row['summary'],
                        'count': row['count'],
                        'data': row['wordcounter'],
                        'source': row['document']}
                    )

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

    def count_words_dicts(self, sourcedict, countfield):
        temp = pd.Series(np.zeros((len(sourcedict[countfield]))))
        for term in self.searchword:
            temp += self.adddata.loc[:, countfield].apply(lambda x: findvalue(dictio=x, key=term))
        return temp

    def create_wcimage(self, counter):
        wc_img = WordCloud(
            background_color="white",
            # width=700,
            # height=500,
            width=500,
            height=350,
            colormap="Dark2",
            # max_words=50,
            max_font_size=30
        ).generate_from_frequencies(
            frequencies=counter
        ).to_image()
        # convert the PIL image to bytes array
        with BytesIO() as output:
            with wc_img as img:
                img.save(output, 'png')
            data = output.getvalue()
        # encode the bytes array representation of the word cloude image
        encoded_image = base64.b64encode(data)
        # return the image for rendering
        return 'data:image/png;base64,{}'.format(encoded_image.decode())
