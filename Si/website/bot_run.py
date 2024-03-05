import random
import json
import pickle
import numpy as np
from tensorflow import keras


import nltk
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer

# to reduce a word to its stem/base form
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('Si/website/bot_intents.json').read()) #to load JSON 

#loading required files and model
words = pickle.load(open('words.pkl','rb')) #rb = reading binary mode
classes = pickle.load(open('classes.pkl','rb'))
model = keras.models.load_model('chatbotmodel.h5') 

#tokenize input and reduce to stem
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#convert a sentence into a bage of words (list 0,1 to know if word is there or not)
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

#to predict the class using the model
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25 #  25% for uncertaininty
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]  #enumerate is to get the class
   
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})
    return return_list

#takes the predicted intents
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    #generate random response
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
        else:
            result = "I do not understand"
    return result

#function to take user input, generate response and return the generated response
def result(val):
    val = val.lower()
    while True:
        ints = predict_class(val)
        res = get_response(ints, intents)
        return res