import logging, json
import azure.functions as func
import aiohttp 
import asyncio
import itertools
from shared_code.utils import load_yaml
from shared_code import dbUtils
from shared_code.commonClasses import Configuration

try:
    cfg = load_yaml("./creativesFromUrl/config.yaml")
except:
    cfg = load_yaml("../creativesFromUrl/config.yaml")

config = Configuration(cfg)

async def download(session, payload):
    url = config.shutterstock["download_format"].format(config.shutterstock["endpoint"])
    headers = {
            'Authorization': f'Bearer {config.shutterstock["token"]}',
            'Content-Type': 'application/json'
    }
    async with session.post(url=url, headers=headers, json=payload) as response:
                resp = json.loads(await response.read())
                logging.info(f'downloaded images: {resp}')
                ret = [{"license_id": element["license_id"], "url": element["download"]["url"], "image_id": element["image_id"]} for element in resp["data"]]
    return ret

async def redownloadImage (session, license_id):
    redownload_url = config.shutterstock["redownload_format"].format(config.shutterstock["endpoint"], license_id)

    header = {
            'Authorization': f'Bearer {config.shutterstock["token"]}'
        }
    payload = {
    "size": "huge"
    }
    
    async with session.post(url=redownload_url, headers=header, json=payload) as response:
        resp = json.loads(await response.read())
        logging.info(f're-download url is: {redownload_url}re-downloaded images: {resp}')
    return resp["url"]

def isLicensed(id):
    lisence = dbUtils.get_image_lisence_by_stockId(id)
    logging.info(f"the row is {lisence}")
    return lisence
    
async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('start downloading process')
    req_body = req.get_json()
    ids = req_body['ids']
    logging.info(f'type of ids is: {type(ids)}the ids are: {ids}')
    
    licensedImages = []
    removedIds = []
    for id in ids:
        lisence = isLicensed(id)
        if lisence != None:
            licensedImages.append(lisence)
            removedIds.append(id)
    ids = [id for id in ids if (id not in removedIds)]
    
    payload = {
    'images': [
        {
            'image_id': id,
            "subscription_id": config.shutterstock["subscription"],
            "price": 0,
            "metadata": {
                "customer_id": "any string"
            }
        }
    for id in ids],
}
    logging.info(f'payload is: {payload}')
    
    async with aiohttp.ClientSession() as session:
        redownloadedImages = await asyncio.gather(*map(redownloadImage, itertools.repeat(session), licensedImages))
        logging.info(f'redownloaded list is: {redownloadedImages}')   
        if config.shutterstock["enable_download"]:
            downloadedImages= await download(session, payload)
            logging.info(f'downloaded images: {downloadedImages}')
            for dImage in downloadedImages:
                dbUtils.update_image_lisence(image_id=dImage["image_id"] , lisence=dImage["license_id"])
            urls = sum([redownloadedImages, [element["url"] for element in downloadedImages]], [])
            logging.info(f'final download urls are: {urls}')
            logging.info('finish downloading process')
            return func.HttpResponse(json.dumps(urls))
        
    return func.HttpResponse('ok', status_code=200)