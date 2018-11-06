#method to use?
with open(datafile, 'w', newline='') as csvfile:
    fieldnames = ['gemeente', 'organisatie', 'locatie', 'naam', 'titel', 'data', 'klasse', 'startdatum', 'einddatum']
    writer = csv.DictWriter(csvfile, delimiter ='|', fieldnames=fieldnames)
    writer.writeheader()

    gemeentelijst = ['aalsmeer','bodegravenreeuwijk',  'alkmaar', 'almelo', 'almere', 'amersfoort', 'amstelveen', 'amsterdam', 'arnhem', 'baarn', 'barneveld', 'beemster', 'binnenmaas', 
                     'borne', 'boxmeer', 'buren', 'castricum', 'culemborg', 'deventer', 'dewolden', 'diemen', 'doetinchem', 'dongen', 'drimmelen', 'edamvolendam', 'ede', 'emmen', 'enschede', 
                     'epe', 'ettenleur', 'goirle', 'gouda', 'groningen', 'hardenberg', 'heemskerk', 'heerde', 'hendrikidoambacht', 'hilvarenbeek', 'hilversum', 'hollandskroon', 'hulst', 
                     'katwijk', 'krimpenerwaard', 'landsmeer', 'leeuwarden', 'leiden', 'leiderdorp', 'leusden', 'lingewaard', 'loonopzand', 'losser', 'maassluis', 'maastricht', 'medemblik', 
                     'meierijstad', 'meppel', 'moerdijk', 'molenwaard', 'nieuwegein', 'nieuwkoop', 'nijkerk', 'noordoostpolder', 'noordwijk', 'noordwijkerhout', 'oisterwijk', 'oldambt', 
                     'ommen', 'oosterhout', 'oostgelre', 'oss', 'overbetuwe', 'raalte', 'rheden', 'rhenen', 'rijswijk', 'roermond', 'roosendaal', 'rucphen', 'schagen', 'schiedam', 'soest', 
                     'staphorst', 'steenbergen', 'steenwijkerland', 'stichtsevecht', 'texel', 'teylingen', 'utrecht', 'veenendaal', 'velsen', 'vlaardingen', 'vlissingen', 'voorst', 
                     'waalwijk', 'wageningen', 'zaanstad', 'zandvoort', 'zeist', 'zoetermeer', 'zwartewaterland', 'zwolle']
    for gemeente in gemeentelijst:
        print(gemeente)
        parameters = {"from": "0"}
        took = 0
        r = requests.get("http://api.openraadsinformatie.nl/v0/" + gemeente +"/events/search", params=parameters)
        data = r.json()
       
        total = data["meta"]["total"]
        if total >= 10000: #Can only load 10.000 documents from API with this function, which is enough as well
            total = 9999
           
        while total > took:
            r = requests.get("http://api.openraadsinformatie.nl/v0/" + gemeente +"/events/search", params=parameters)
            try:
                data = r.json()
                took += 10
                parameters["from"] = str(took)
        
                for article in data[u"events"]:
                    if u"organization_id" in article.keys() and u"location" in article.keys() and u"name" in article.keys() and u"description" in article.keys() and u"classification" in article.keys() and u"start_date" in article.keys() and u"end_date" in article.keys() and u"classification" in article.keys() and u"classification" in article.keys():
                         writer.writerow({'gemeente': gemeente,
                                         'organisatie': article[u"organization_id"].encode('utf-8'),
                                         'locatie': article[u"location"].encode('utf-8'),
                                         'titel': article[u"name"].encode('utf-8'),
                                         'data': str(article[u"description"].encode('utf-8')).replace("\\n", " ").replace("\\u", " ").replace("\\r", " "),
                                         'klasse': str(article[u"classification"].encode('utf-8')).replace("\\n", " ").replace("\\u", " ").replace("\\r", " "),
                                         'startdatum': article[u"start_date"].encode('utf-8'),
                                         'einddatum': article[u"end_date"].encode('utf-8')})
            except:
                took=9999
