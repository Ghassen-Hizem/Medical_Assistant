
from django.http import HttpResponse
import pickle
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from django.views.decorators.csrf import csrf_exempt
import json

#label encoder
le_path = "../Pretrained_model/label_encoder.pkl"

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

@csrf_exempt

def index(request):

    if request.method == 'POST':
        symptoms = json.loads(request.body.decode('utf-8'))['text']
        symptoms = symptoms.strip().split(",")
        text = ", ".join(symptoms)
        inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()
        predicted_disease = le.inverse_transform([predicted_label])[0]
        print("You probably have", predicted_disease,'!')
        print(disease_des.loc[disease_des.Disease==predicted_disease].Description.iloc[0])
        print('Precautions:')
        print('1/',disease_precautions.loc[disease_precautions.Disease==predicted_disease].Precaution_1.iloc[0])
        print('2/',disease_precautions.loc[disease_precautions.Disease==predicted_disease].Precaution_2.iloc[0])
        print('3/',disease_precautions.loc[disease_precautions.Disease==predicted_disease].Precaution_3.iloc[0])
        print('4/',disease_precautions.loc[disease_precautions.Disease==predicted_disease].Precaution_4.iloc[0])
    
    
    return  HttpResponse("Post request not sent correctly !")


