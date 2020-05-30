import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils
# Plus l'erreur de librairie et plus le warning sur le fait que TensorFlow n'a pas été compilé pour mon type de processeur
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
# On configure le nombre de CPU par type de threads pour maximiser les performances
from keras import backend as K
import tensorflow as tf
config = tf.ConfigProto(device_count={"CPU":2},
						inter_op_parallelism_threads=2,
						intra_op_parallelism_threads=2)
session = tf.Session(config=config)
K.set_session(session)

# Load le texte
filename = "macbeth.txt"

text = (open(filename).read()).lower()

# On récupère tout les caractères possibles du texte que l'on tri dans une liste
unique_chars = sorted(list(set(text)))

char_to_int = {}
int_to_char = {}
# Tout les caractères ont maintenant leur valeur égale en char et en int
# Integer encoding or label encoding (une valeur char est associé à une valeur numérique)
for i, c in enumerate (unique_chars):
    char_to_int.update({c: i})
    int_to_char.update({i: c})

# Prépare les données input et output
# On prépare 49 items dans X et le 50ème dans Y, c'est-à-dire, la fin du message/mot des 49 items de X
# Par exemple "'H' 'E' 'L' 'L'" en input et "'O'" en output
X = []
Y = []
for i in range(0, len(text) - 50, 1):
    sequence = text[i:i + 50]
    label = text[i + 50]
    X.append([char_to_int[char] for char in sequence])
    Y.append(char_to_int[label])

# On reshape les données pour leur données une structure adéquate au NN, avec un triplet
# Le triplet comporte la taille de nos données, le nombre d'étape pour une donnée (time steps) et le nombre de variables que l'on a correpondant à la vrai valeur Y
# On normalise les valeurs que l'on fournit au NN
# One hot Encoder (permet de transformer des Categorical Data (sous forme de catégorie plutôt écrit) en numerical data)
# Pour chaque unique valeur int on affecte une variable binaire, permet de classer une catégorie numériquement
X_modified = numpy.reshape(X, (len(X), 50, 1))
X_modified = X_modified / float(len(unique_chars))
Y_modified = np_utils.to_categorical(Y)

# On définit le modèle
# Un layer LSTM avec 300 neurones, les données doivent être en format (50,1) et on retourne la séquence pour pas que le layer suivant recoive des données random
# Ensuite un layer Dropout pour éviter l'overfitting. Puis encore une LSTM avec 300 neurones et encore un Dropout
# Puis un layer Dense (fully connected layer) avec une fonction d'acrivation softmax avec un neurone car on renvoit un unique caractère
# Puis la compilation du modèle
model = Sequential()
model.add(LSTM(300, input_shape=(X_modified.shape[1], X_modified.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(300))
model.add(Dropout(0.2))
model.add(Dense(Y_modified.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# On entraîne le modèle avec les données
model.fit(X_modified, Y_modified, epochs=1, batch_size=30)

# On créer une random seed pour facilement reproduire le résultat
start_index = numpy.random.randint(0, len(X)-1)
new_string = X[start_index]

# Gènere des caractères avec les prédictions du modèles
for i in range(50):
    x = numpy.reshape(new_string, (1, len(new_string), 1))
    x = x / float(len(unique_chars))

    # Prédictions et on décode la prédictions pour l'afficher en alphabet
    pred_index = numpy.argmax(model.predict(x, verbose=0))
    char_out = int_to_char[pred_index]
    seq_in = [int_to_char[value] for value in new_string]
    print(char_out)

    new_string.append(pred_index)
    new_string = new_string[1:len(new_string)]