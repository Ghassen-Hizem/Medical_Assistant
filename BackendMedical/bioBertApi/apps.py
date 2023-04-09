from django.apps import AppConfig
import html
import pathlib
import os

from bioBertApi.model import Bert

#TO_DO 
class BiobertapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bioBertApi'
    MODEL_PATH = pathlib.Path("model")
    BERT_PRETRAINED_PATH = Path("model")
