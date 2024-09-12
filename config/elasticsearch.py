from elasticsearch import Elasticsearch
from decouple import config

ELASTIC_URL = config("ELASTIC_URL", cast=str)

es = Elasticsearch([ELASTIC_URL])
