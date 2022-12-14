#!/usr/bin/env python
# coding: utf-8

# ### `Name : Berchmans Kevin S`

# ## `Text Classification using CNN-LSTM and Pre-trained IMDB Models`

# In[1]:


import tensorflow as tf 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import nltk
from sklearn.model_selection import train_test_split 
from tensorflow.keras.preprocessing. text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences 
from tensorflow.keras.optimizers import RMSprop , Adam
from keras.models import Sequential
from keras.layers import *
from nltk.corpus import stopwords 
nltk.download('stopwords') 
",".join(stopwords.words('english'))
STOPWORDS = set(stopwords.words('english'))


# In[2]:


data = pd.read_csv("IMDB Dataset.csv")
data.head()


# In[3]:


data.tail()


# In[4]:


data.shape


# In[5]:


data.size


# In[6]:


data.info()


# In[7]:


data.describe()


# In[8]:


y =data['sentiment'] 
X=[] 
for review in data['review']: 
    filtered_sentence = [w.lower() for w in review.split() if not w in STOPWORDS ] 
    X.append(filtered_sentence)
X = pd.Series(X) 


# In[9]:


y_tokenizer = Tokenizer() 
y_tokenizer.fit_on_texts(y) 
y_seq = np.array(y_tokenizer.texts_to_sequences (y))


# In[10]:


X_token = Tokenizer(num_words=5000,oov_token='<oov>') 
X_token.fit_on_texts(X) 
word_index = X_token.word_index
X_sequence = X_token.texts_to_sequences(X) 
dict(list(word_index.items())[0:15])


# In[11]:


X_padding= pad_sequences(X_sequence, maxlen=200, padding='post') 


# In[12]:


print(y_seq.shape) 
print(X_padding.shape) 


# In[13]:


x_train,x_test,y_train,y_test = train_test_split(X_padding, y_seq,train_size=0.7)


# In[14]:


print(x_train.shape, x_test.shape) 
print(y_train.shape, y_test.shape)


# In[15]:


vocab_size = 5000 
embedding_dim = 64 
max_length = 200


# In[16]:


model1 = Sequential() 
model1.add(Embedding(vocab_size, embedding_dim)) 
model1.add(LSTM(embedding_dim))
model1.add(Dense(embedding_dim, activation='tanh'))
model1.add(Dense(6,activation='softmax'))


# In[17]:


model1. summary()


# In[18]:


model1.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])


# In[19]:


history1 = model1.fit(x_train,y_train, epochs=20, verbose=2, validation_split=0.2)


# In[20]:


plt.plot(history1.history['accuracy']) 
plt.plot(history1.history['val_accuracy'])
plt.title('model accuarcy') 
plt.xlabel('accuracy') 
plt.ylabel('epoch') 
plt.legend(['train', 'validation'])
plt.show()


# In[21]:


plt.plot(history1.history['loss']) 
plt.plot(history1.history['val_loss'])

plt.title('model loss') 
plt.xlabel('loss') 
plt.ylabel('epoch') 
plt.legend(['train', 'validation'])
plt.show() 


# In[22]:


print("loss: ", model1.evaluate(x_test,y_test, verbose=0)[0]) 
print("accuarcy: ", model1.evaluate(x_test, y_test, verbose=0)[1]) 


# In[23]:


model2 = Sequential() 
model2.add(Embedding(vocab_size, embedding_dim)) 
model2.add(Conv1D(filters=32, kernel_size=5, strides=1, activation='relu'))
model2.add(MaxPooling1D((2))) 
model2.add(LSTM(embedding_dim)) 
model2.add(Dense(128, activation= 'relu'))
model2.add(Dense(6, activation='softmax')) 


# In[24]:


model2. summary()


# In[25]:


model2.compile (optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['accuracy'])


# In[26]:


history2 = model2.fit(x_train,y_train, epochs=20,validation_split=0.2, verbose=2) 


# In[27]:


plt.plot(history2.history['accuracy']) 
plt.plot(history2.history['val_accuracy']) 
plt.title('model accuarcy') 
plt.xlabel('accuracy') 
plt.ylabel('epoch') 
plt.legend(['train', 'validation'])
plt.show() 


# In[28]:


plt.plot(history2.history['loss']) 
plt.plot(history2.history['val_loss']) 
plt.title('model loss')
plt.xlabel('loss') 
plt.ylabel('epoch') 
plt.legend(['train', 'validation']) 
plt.show() 


# In[29]:


score = model2.evaluate(x_test,y_test,verbose=0) 
print("loss: ", score[0]) 
print("accuracy: ", score[1])


# In[ ]:




