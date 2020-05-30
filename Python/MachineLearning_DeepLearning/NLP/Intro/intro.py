import nltk
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

# On récupère la page
response =  urllib.request.urlopen('https://en.wikipedia.org/wiki/SpaceX')
html = response.read()
# On récupère le texte pour avoir qqchose d'un peu plus propre
soup = BeautifulSoup(html,'html.parser')
text = soup.get_text(strip = True)

# On convertit en Tokens (on récupère les mots, chaque mot est un élément de la liste)
tokens = [t for t in text.split()]

sr= stopwords.words('english')
clean_tokens = tokens[:]
for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)

freq = nltk.FreqDist(clean_tokens)
for key,val in freq.items():
    print(str(key) + ':' + str(val))

freq.plot(20, cumulative=False)