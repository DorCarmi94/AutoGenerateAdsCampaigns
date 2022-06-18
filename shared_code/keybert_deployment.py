import logging
from keybert import KeyBERT
import os, sys
sys.path.append(os.getenv('AZUREML_MODEL_DIR'))

def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model
    model = KeyBERT()
    logging.info("Init complete")

def run(text, range, n):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(range[0], range[1]), top_n=n)
    return keywords