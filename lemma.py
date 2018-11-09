import requests


class Lemma(object):
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({'referer': 'http://woordenlijst.org/'})
        self.url = "http://woordenlijst.org/api-proxy/"
        self.params = {
            'm': 'search',
            'tactical': 'true'
        }

    def get_lemmas(self, word):
        self.params['searchValue'] = word
        r = self.s.get(url=self.url, params=self.params)

        if r.status_code == 200:
            return [(entry['lemma'], entry['type']) for entry in r.json()["_embedded"]["exact"]]
        else:
            return []


if __name__ =="__main__":
    lemma = Lemma()
    print(lemma.get_lemmas('boompje'))