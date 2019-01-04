from __future__ import print_function
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb
from keras.utils.np_utils import to_categorical
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras.callbacks import CSVLogger
import keras
import keras.preprocessing.text
import itertools
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
from keras import callbacks
from keras.layers import recurrent
from keras.initializations import normal, identity
from keras.optimizers import RMSprop
learning_rate = 0.1
trainlabels = pd.read_csv('dgcorrect/trainlabel.csv', header=None)

trainlabel = trainlabels.iloc[:,0:1]

testlabels = pd.read_csv('dgcorrect/testlabel.csv', header=None)

testlabel = testlabels.iloc[:,0:1]


train = pd.read_csv('dgcorrect/train.txt', header=None)
test = pd.read_csv('dgcorrect/test.txt', header=None)


X = train.values.tolist()
X = list(itertools.chain(*X))


T = test.values.tolist()
T = list(itertools.chain(*T))



 # Generate a dictionary of valid characters
valid_chars = {x:idx+1 for idx, x in enumerate(set(''.join(X)))}

max_features = len(valid_chars) + 1
maxlen = np.max([len(x) for x in X])
print(maxlen)
# Convert characters to int and pad
X = [[valid_chars[y] for y in x] for x in X]


X_train = sequence.pad_sequences(X, maxlen=maxlen)

max_len = 37
# Generate a dictionary of valid characters
valid_chars = {x:idx+1 for idx, x in enumerate(set(''.join(T)))}

max_features = len(valid_chars) + 1
maxlen = np.max([len(x) for x in T])
print(maxlen)
# Convert characters to int and pad
T = [[valid_chars[y] for y in x] for x in T]


X_test = sequence.pad_sequences(T, maxlen=max_len)


y_train1 = np.array(trainlabel)
y_train= to_categorical(y_train1)
print(y_train.shape)
y_test1 = np.array(testlabel)
y_test= to_categorical(y_test1)
print(y_test.shape)

embedding_vecor_length = 128

'''
model = Sequential()
model.add(Embedding(max_features, embedding_vecor_length, input_length=max_len))
model.add(LSTM(128))
model.add(Dropout(0.1))
model.add(Dense(18))
model.add(Activation('softmax'))
'''

# 1. define the network
model = Sequential()
model.add(Embedding(max_features, embedding_vecor_length, input_length=max_len))
model.add(SimpleRNN(128,init=lambda shape, name: normal(shape, scale=0.001, name=name),inner_init=lambda shape, name: identity(shape, scale=1.0, name=name),activation='relu',))  # try using a GRU instead, for fun
#model.add(Dropout(0.1))
model.add(Dense(18))
model.add(Activation('softmax'))
rmsprop = RMSprop(lr=learning_rate)


model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
checkpointer = callbacks.ModelCheckpoint(filepath="logs/irnn/checkpoint-{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='val_acc',mode='max')
csv_logger = CSVLogger('logs/irnn/training_set_lstmanalysis.csv',separator=',', append=False)
model.fit(X_train, y_train, batch_size=32, nb_epoch=1000,validation_split=0.33, shuffle=True,callbacks=[checkpointer,csv_logger])
score, acc = model.evaluate(X_test, y_test, batch_size=32)
print('Test score:', score)
print('Test accuracy:', acc)


