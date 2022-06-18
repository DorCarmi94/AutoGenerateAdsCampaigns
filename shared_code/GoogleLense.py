import json
import os
import aiohttp 
import base64
import logging
import asyncio
from distutils.command.config import config
from shared_code.commonClasses import Configuration
from shared_code.utils import load_yaml

try:
    cfg = load_yaml("./creativesFromUrl/config.yaml")
except:
    cfg = load_yaml("../creativesFromUrl/config.yaml")
config = Configuration(cfg)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.google_lense["app_credentials"] 
google_url = config.google_lense["format"].format(config.google_lense["endpoint"], config.google_lense["key"])

async def getImageBase64(session, url):
    async with session.get(url= url) as image_response:
        image_resp = await image_response.content.read()
        content = base64.b64encode(image_resp).decode('UTF-8')
        
        return content
    
async def detectLables(session, payload, headers):
    async with session.post(url= google_url, json= payload, headers= headers) as response:
        resp = json.loads(await response.read())

        return resp

async def imagesLables(images):
    logging.info('images Lables')
    headers = {
                'Authorization': 'Bearer ',
                'Content-Type': 'application/json; charset=utf-8',
    }
    
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop= loop) as session:
        contents =  await asyncio.gather(*[getImageBase64(session, url) for url in images], return_exceptions=True)
        logging.info('done gathering images contents')
    
        reqs = [
                {
                    "image": {
                        "content": contnet
                    },
                    "features": [
                        {
                            "maxResults": config.google_lense["n_google_lables"],
                            "type": "LABEL_DETECTION"
                        }
                    ]
                }
                for contnet in contents
            ]
            
        payload = {
            "requests": reqs
        }
        
        logging.info('time 1')
        results =  await detectLables(session, payload, headers)
        results = results['responses']
        logging.info('time 2')
        ret = {}
        for pos in range(len(results)):
            image_data = []
            for lable in results[pos]['labelAnnotations']:
                image_data.append([lable["description"], lable["score"]])
            ret[images[pos]] = image_data

        return ret
