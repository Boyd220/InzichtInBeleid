import pickle

# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.probability import FreqDist

with open('save.p', 'rb') as f:
    events = pickle.load(f)

# gooit alle tekst in een string
# TODO tekst per gemeente opslaan
# TODO total_text dumpen
total_text = ''
n = 0
for event in events:
    if 'sources' in event:
        for source in event['sources']:
            if 'description' in source and source['description']:
                total_text += source['description']
                n += 1
print(n)

sw = set(stopwords.words('dutch')) # voor nu nltk stopwords
# maak freq dist
freq_dist = FreqDist(word for word in total_text.lower().replace('.', '').split() if word not in sw and len(word) > 2)


r = 0.005 # het aandeel hoogste en laagste rangen dat wordt weggegooid (speel hiermee)
l = len(freq_dist)
m = int(r*l)

# gooit de m hoogste en laagste rangen weg
# TODO frequentie meenemen in berekening (dus een deel van de prob. mass. weggooien ipv rangen)
middle_mass = freq_dist.most_common()[m:l-m]
print(middle_mass[:100])