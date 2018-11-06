import requests
import pandas as pd
import json
import datetime
from openpyxl import load_workbook
# import matplotlib.pyplot as plt




def query_ori_df(query, data_range):
    base = 'http://api.openraadsinformatie.nl/v0/search/events'
    data = {"query": query,
            "filters": {"start_date": data_range},
            "facets": {
                "collection": {'size': 100000}
            },
            'size': 0}

    r = requests.post(base, data=json.dumps(data))
    if r.status_code == 200:
        # print(r.json()['facets']['collection']['sum_other_doc_count'])
        return filter_municipalities(r.json()['facets']['collection']['buckets'])
    else:
        raise Exception(r.text)

# def plot_maps()


def filter_municipalities(doc_counts):
    base = 'http://api.openraadsinformatie.nl/v0/search/organizations'
    r = requests.post(base, data=json.dumps({"query": "",
                                             "filters": {"classification": {"terms": ["Municipality"]}},
                                             'size': 500}))

    if r.status_code == 200:
        gemeenten = [(org['meta']['collection'], org['identifiers'], org['name']) for org in r.json()['organizations']]
        gemeenten = {gemeente[0]: ([cbs_id['identifier'] for cbs_id in gemeente[1] if cbs_id['scheme'] == 'CBS'], gemeente[2] )for
                     gemeente in gemeenten}

        results = {gemeenten[item['key']][1]: {'count': item['doc_count'], 'cbs_id': gemeenten[item['key']][0][0] if len(item['key']) > 0
        else None} for item in doc_counts if item['key'] in gemeenten}

        return pd.DataFrame(results).transpose()
    else:
        raise Exception(r.text)

def search(query, file=None):
    today = datetime.date.today()

    this_year = query_ori_df(query, {"from": str(today.year) + "-01-01",
                                     "to": str(today)})

    this_month = query_ori_df(query, {"from": str(today.year) + "-" + str(today.month) + "-01",
                                      "to": str(today)})

    # print(this_month)
    df = this_year.join(this_month, how='outer', rsuffix='_month').fillna(0).drop('cbs_id_month', axis=1)
    df.columns = ['cbs_id', 'dit jaar', 'deze maand']

    print(df)
    if file:
        book = load_workbook(file)
        writer = pd.ExcelWriter(file, engine='openpyxl')
        writer.book = book

        df[['dit jaar', 'deze maand']].to_excel(writer, 'open raads informatie')
        writer.sheets['open raads informatie'].column_dimensions['A'].width = 30
        writer.sheets['open raads informatie'].column_dimensions['B'].width = 15
        writer.sheets['open raads informatie'].column_dimensions['C'].width = 15

        writer.save()

    # plt.title(query)
    # plt.show()

if __name__ == "__main__":
    search("omgevingswet")
