from channels.generic.websocket import AsyncJsonWebsocketConsumer
import pickle
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification

#label encoder
with open("/home/hizem/Desktop/Medical_Assistant/BackendMedical/Pretrained_model/label_encoder.pkl", 'rb') as file:
    le = pickle.load(file)

#model and tokenizer loading
model_dir_path = 'Pretrained_model/BioBERT_model'
tokenizer = AutoTokenizer.from_pretrained(model_dir_path)
model = AutoModelForSequenceClassification.from_pretrained(model_dir_path)
#loading data

data = pd.read_csv('/home/hizem/Desktop/Medical_Assistant/BackendMedical/Data/DataML/dataset.csv') 
disease_des=pd.read_csv('/home/hizem/Desktop/Medical_Assistant/BackendMedical/Data/DataML/symptom_Description.csv')
disease_precautions=pd.read_csv('/home/hizem/Desktop/Medical_Assistant/BackendMedical/Data/DataML/symptom_precaution.csv')

class PracticeConsumer(AsyncJsonWebsocketConsumer):

      async def connect(self):
           await self.accept()

      async def receive(self, text_data=None, bytes_data=None, **kwargs):
            symptoms = text_data
            symptoms = symptoms.strip().split(",")
            text = ", ".join(symptoms)
            inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
            outputs = model(**inputs)
            predicted_label = torch.argmax(outputs.logits, dim=1).item()
            predicted_disease = le.inverse_transform([predicted_label])[0]
            ch = "You probably have  " + predicted_disease + "\n"
            ch = ch + disease_des.loc[disease_des.Disease==predicted_disease].Description.iloc[0] + "\n"
            ch = ch + "Precautions:" + "\n"
            ch = ch + "1/" + disease_precautions.loc[disease_precautions.Disease==predicted_disease].Precaution_1.iloc[0] + "\n"
            ch = ch + "2/" + disease_precautions.loc[disease_precautions.Disease==predicted_disease].Precaution_2.iloc[0] + "\n"
            ch = ch + "3/" + disease_precautions.loc[disease_precautions.Disease==predicted_disease].Precaution_3.iloc[0] + "\n"
            ch = ch + "4/" + disease_precautions.loc[disease_precautions.Disease==predicted_disease].Precaution_4.iloc[0] + "\n"
            print(ch)
            await self.send(ch)