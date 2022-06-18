import logging, json
import asyncio
import aiohttp 
import copy
from shared_code.utils import load_yaml
from shared_code.commonClasses import Configuration

try:
    cfg = load_yaml("./creativesFromUrl/config.yaml")
except:
    cfg = load_yaml("../creativesFromUrl/config.yaml")

config = Configuration(cfg)

def lensOfQuery(kws):
    curr_lens = 0
    for kw in kws:
        curr_lens += len(kw)
    curr_lens = curr_lens + len(kws)
    return curr_lens

def validPixabayKws(kws):
    curr_lens = lensOfQuery(kws)
    while curr_lens > 100:
        kws.pop()
        curr_lens = lensOfQuery(kws)
    return kws

async def getImages_pixabay(session, kw, n):
    if not config.pixabay["enabled"]:
        return []
    pixabay_kw = copy.deepcopy(kw)
    for i in range(len(pixabay_kw)):
        pixabay_kw[i] = '(' + pixabay_kw[i] + ')'
    pixabay_kw = validPixabayKws(pixabay_kw)
    q_parameter = "|".join(pixabay_kw)
    pixabay_url = config.pixabay["format"].format(config.pixabay["endpoint"], config.pixabay["key"], q_parameter)

    async with session.get(url=pixabay_url) as response:
        try:
            resp = json.loads(await response.read())
            images_p = [x["largeImageURL"] for x in resp["hits"][:n]]
            logging.info(f'first {resp}')
        except:
            images_p = []
        
        return images_p

async def getImages_shutterstock(session, kw, n):
    if not config.shutterstock["enabled"]:
        return []
    parent_kw = copy.deepcopy(kw)
    for i in range(len(parent_kw)):
        parent_kw[i] = '(' + parent_kw[i] + ')'
    q_parameter = "OR".join(parent_kw)
    shutterstock_url = config.shutterstock["format"].format(config.shutterstock["endpoint"], q_parameter)
    auth = aiohttp.BasicAuth(login=config.shutterstock["key"], password=config.shutterstock["secret"])
    
    async with session.get(url=shutterstock_url, auth=auth) as response:
        try:
            resp = json.loads(await response.read())
            logging.info(f'shutterstock images: {resp}')
            images_s = [{"id": x["id"], "image": x["assets"]["preview_1500"]["url"]} for x in (resp["data"])[:n]]
            logging.info(f'shutterstock tuples list is:  {images_s}')
        except:
            images_s = []
        
        return images_s
    
async def getImages_pexels(session, kw, n):
    if not config.pexels["enabled"]:
        return []
    q_parameter = " | ".join(kw)
    pexels_url = config.pexels["format"].format(config.pexels["endpoint"], q_parameter, 30, 1)
    pex_params = {'Authorization': config.pexels["key"]}

    async with session.get(url=pexels_url, headers=pex_params) as response:
        try:
            resp = json.loads(await response.read())
            images_pex = []
            images_pex = [json_photo for json_photo in resp["photos"]]
            images_pex = [x['src']['large2x'] for x in images_pex][:n]
            logging.info(f'third {resp}')
        except:
            images_pex = []
        
        return images_pex

        
async def main(req_body):
    logging.info(f'images service starts {req_body}')
    kw = req_body['kw']
    n = int(req_body['n'])
    
    #async requests - pixabay, shutterstock, pexels        
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            getImages_pixabay(session, kw, n),
            getImages_shutterstock(session, kw, n),
            getImages_pexels(session, kw, n)
        )
        
        images = sum([results[0], [x["image"] for x in results[1]], results[2]], [])
        logging.info(f'the final images are:  {images}')
        
    return [images, results[1]]
