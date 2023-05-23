from channels.generic.websocket import AsyncJsonWebsocketConsumer
import pickle
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import nltk
import keras
import json
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
from nltk.corpus import wordnet

model = keras.models.load_model(
    '/home/hizem/Desktop/Medical_Assistant/BackendMedical/Pretrained_model/bot.h5')

tag_response_dict = dict()

with open('/home/hizem/Desktop/Medical_Assistant/BackendMedical/Pretrained_model/intents.json') as file:
    a = json.load(file)

intents = a['intents']

for intent in intents:
    tag_response_dict[intent['tag']] = intent['responses']


# label encoder
with open("/home/hizem/Desktop/Medical_Assistant/BackendMedical/Pretrained_model/label_encoder.pkl", 'rb') as file:
    le = pickle.load(file)

# model and tokenizer loading
model_dir_path = 'Pretrained_model/BioBERT_model'
Btokenizer = AutoTokenizer.from_pretrained(model_dir_path)
diag_model = AutoModelForSequenceClassification.from_pretrained(model_dir_path)
# loading data

data = pd.read_csv(
    '/home/hizem/Desktop/Medical_Assistant/BackendMedical/Data/DataML/dataset.csv')
disease_des = pd.read_csv(
    '/home/hizem/Desktop/Medical_Assistant/BackendMedical/Data/DataML/symptom_Description.csv')
disease_precautions = pd.read_csv(
    '/home/hizem/Desktop/Medical_Assistant/BackendMedical/Data/DataML/symptom_precaution.csv')


with open('/home/hizem/Desktop/Medical_Assistant/BackendMedical/Pretrained_model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

oneHotEncoder = OneHotEncoder()


def synonym_replacement(sentence):
    """
    Replace words in a sentence with their synonyms
    """
    words = nltk.word_tokenize(sentence)
    new_words = words.copy()
    for i in range(len(words)):
        if wordnet.synsets(words[i]):
            synonyms = wordnet.synsets(words[i])[0].lemmas()
            if len(synonyms) > 1:
                new_words[i] = synonyms[random.randint(
                    0, len(synonyms)-1)].name()
    return ' '.join(new_words)


def random_insertion(sentence):
    """
    Insert a random word into a sentence
    """
    words = nltk.word_tokenize(sentence)
    new_words = words.copy()
    for i in range(3):
        index = random.randint(0, len(words)-1)
        new_words.insert(index, wordnet.synset(
            'entity.n.01').lemmas()[0].name())
    return ' '.join(new_words)


def random_deletion(sentence):
    """
    Delete a random word from a sentence
    """
    words = nltk.word_tokenize(sentence)
    new_words = words.copy()
    index = random.randint(0, len(words)-1)
    new_words.pop(index)
    return ' '.join(new_words)


def random_swap(sentence):
    """
    Swap two random words in a sentence
    """
    words = nltk.word_tokenize(sentence)
    new_words = words.copy()
    index1 = random.randint(0, len(words)-1)
    index2 = random.randint(0, len(words)-1)
    new_words[index1], new_words[index2] = new_words[index2], new_words[index1]
    return ' '.join(new_words)


words, labels, docs, outputs = [], [], [], []
for intent in intents:
    for pattern in intent['patterns']:
        docs.append(pattern)
        docs.append(random_deletion(pattern))
        docs.append(random_insertion(pattern))
        docs.append(random_swap(pattern))
        docs.append(synonym_replacement(pattern))
        outputs.append(intent['tag'])
        outputs.append(intent['tag'])
        outputs.append(intent['tag'])
        outputs.append(intent['tag'])
        outputs.append(intent['tag'])
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

y = oneHotEncoder.fit_transform([[label] for label in outputs]).toarray()


class PracticeConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        symptoms = text_data
        symptoms = symptoms.strip().split(",")
        text = ", ".join(symptoms)

        def diagnosis(text, data=data, disease_des=disease_des, disease_precautions=disease_precautions, le=le, tokenizer=tokenizer, diag_model=diag_model):

            # Tokenize the text input
            inputs = Btokenizer(text, padding=True, truncation=True,
                                max_length=512, return_tensors="pt")
            outputs = diag_model(**inputs)
            predicted_label = torch.argmax(outputs.logits, dim=1).item()
            predicted_disease = le.inverse_transform([predicted_label])[0]
            ch = "You probably have  " + predicted_disease + "\n"
            ch = ch + disease_des.loc[disease_des.Disease ==
                                      predicted_disease].Description.iloc[0] + "\n"
            ch = ch + "Precautions:" + "\n"
            ch = ch + "1/" + \
                disease_precautions.loc[disease_precautions.Disease ==
                                        predicted_disease].Precaution_1.iloc[0] + "\n"
            ch = ch + "2/" + \
                disease_precautions.loc[disease_precautions.Disease ==
                                        predicted_disease].Precaution_2.iloc[0] + "\n"
            ch = ch + "3/" + \
                disease_precautions.loc[disease_precautions.Disease ==
                                        predicted_disease].Precaution_3.iloc[0] + "\n"
            ch = ch + "4/" + \
                disease_precautions.loc[disease_precautions.Disease ==
                                        predicted_disease].Precaution_4.iloc[0] + "\n"
            return ch

        def bot(text, tag_response_dict=tag_response_dict, tokenizer=tokenizer, Btokenizer=Btokenizer, model=model, leng=18):
            text_p = []
            prediction_input = [message.lower().translate(
                str.maketrans('', '', string.punctuation)) for message in text]
            prediction_input = ''.join(prediction_input)
            text_p.append(prediction_input)
            prediction_input = tokenizer.texts_to_sequences(text_p)
            prediction_input = np.array(prediction_input).reshape(-1)
            prediction_input = pad_sequences([prediction_input], 18)

            pred = model.predict(prediction_input)

            predicted_class = oneHotEncoder.inverse_transform(pred)
            response = random.choice(tag_response_dict[predicted_class[0][0]])
            if predicted_class[0][0] == 'diagnosis':
                return diagnosis(text)
            else:
                return response

        await self.send(bot(text))
