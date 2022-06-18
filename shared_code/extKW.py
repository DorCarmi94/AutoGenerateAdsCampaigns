import logging, json, requests
import azure.functions as func

def main(text):
    url = 'https://kb2.centralus.inference.ml.azure.com/score'
    api_key = 'II8LMF8VOzbhed4WwYdd4rMcKp1aJcZ3'
    headers = {
        'Content-Type':  'application/json', 
        'Authorization': ('Bearer '+ api_key)
    }
    response = requests.post(url, headers=headers, json=text)
    logging.info(f'extKw resp {response.content}, {response.json}')
    keywords = json.loads(response.text)

    return keywords

    