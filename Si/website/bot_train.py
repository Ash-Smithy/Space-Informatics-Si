import random
import json
import pickle
import numpy as np
from tensorflow import keras


import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

# to reduce a word to its stem/base form
lemmatizer = WordNetLemmatizer()

#to load JSON 
intents = json.loads(open('Si/website/bot_intents.json').read())
words = []
classes = []
documents = []
ignore_letters = ['?','!','.',',']

#to extract words from pattens and append to a list
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern) #tokenize is used to break down the words
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#create list of words for chatbot
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words)) #to eliminate dumplicates

#create list of classes for chatbot to recognise
classes = sorted(set(classes))

#dump the created words,classes into pickle files (pickle files convert objects into byte streams)
pickle.dump(words, open('words.pkl', 'wb')) #wb - write binary (to write into the file)
pickle.dump(classes, open('classes.pkl','wb'))


training = []
output_empty = [0] * len(classes)

#Converting words to numerical values for the neural network
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    #to give value if word occurs in the pattern
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)


    output_row = list(output_empty) #copying the list
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

#shuffling the training data to randomize order
random.shuffle(training)
training = np.array(training)

#split training data into input X and output Y
train_x = list(training[:,0])
train_y = list(training[:,1])

#Building the network
model = keras.models.Sequential()
model.add(keras.layers.Dense(128, input_shape=(len(train_x[0]),),activation='relu')) #input layer
model.add(keras.layers.Dropout(0.5)) #to prevent overfitting
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(len(train_y[0]), activation='softmax')) #softmax scales numbers/logits into probabilities
sgd = keras.optimizers.SGD(learning_rate=0.01, weight_decay= 1e-6, momentum=0.9, nesterov=True)  # 1e-6 = 0.000001 
model.compile(loss= 'categorical_crossentropy', optimizer=sgd, metrics= ['accuracy']) #SGD is an algorithm which helps in calculating the gradients for variable to create new values for the variable

#fitting the model
hist = model.fit(np.array(train_x),np.array(train_y),epochs=200, batch_size=5,verbose=1)
model.save('chatbotmodel.h5', hist)
print("done")
