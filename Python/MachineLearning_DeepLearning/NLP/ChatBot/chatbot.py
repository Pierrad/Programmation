# Voir https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e
# Package 'punkt' et 'wordnet' déjà dispo
import nltk
import numpy as np
import random
import string
# Les deux imports en dessous vont permettre de mesurer la similarité entre un mot de l'utilisateur et un mot du corpus
# Permet de convertir une liste de documents brutes en matrices d'objets TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
# Permet d'appliquer la 'cosine similarity', permet de mesurer la ressemblance entre deux vecteurs
from sklearn.metrics.pairwise import cosine_similarity

# WordNet is a semantically-oriented dictionary of English included in NLTK.
lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

# Prend un mot et renvoit sa version normalisé (lemmatize)
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
# Prend du texte et renvoit sa version normalisé (tokenize puis lemmatize)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
# Si la phrase est une salutation, renvoit une salutation
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Fonction de réponse aux messages de l'utilisateur
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    # TF-IDF Approach puis Cosine Similarity
    TfidfVec = TfidfVectorizer(tokenizer = LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


# Ouverture et récupération des données du fichier
f = open('chatbot.txt', 'r', errors = 'ignore')
raw = f.read()

# Convertit en minuscule
raw = raw.lower()

# Convertit en liste de phrases
sent_tokens = nltk.sent_tokenize(raw)
# Convertit en liste de mots
word_tokens = nltk.word_tokenize(raw)

flag=True
print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")

while(flag==True):
    user_response = input()
    user_response = user_response.lower()
    if(user_response != 'bye'):
        if(user_response == 'thanks' or user_response == 'thank you'):
            flag = False
            print("ROBO: You are welcome..")
        else:
            if(greeting(user_response) != None):
                print("ROBO: " + greeting(user_response))
            else:
                print("ROBO: ", end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag = False
        print("ROBO: Bye! take care..")