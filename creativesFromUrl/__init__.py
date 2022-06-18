from ast import keyword
import logging, json, time, datetime
import azure.functions as func
import aiohttp
import asyncio
from shared_code.utils import load_yaml
from shared_code.commonClasses import Image, Title, Configuration
from shared_code import imageScore
from shared_code.keybert_deployment import init, run
from shared_code import scrapeLP
from shared_code import getImages
from shared_code import getTitles
from shared_code import getCat
from shared_code import dbUtils
from shared_code.extKW import main as getKw 

cfg = load_yaml("creativesFromUrl/config.yaml")
config = Configuration(cfg)

async def main(req: func.HttpRequest) -> func.HttpResponse:
    async with aiohttp.ClientSession():
        logging.info('main ad creation function endpoint')
        tcd = datetime.datetime.now()
        t0 = time.time()
        req_body = req.get_json()
        url = req_body["url"]
        logging.info(f"input: {req_body}\ncreatedDate: {tcd.isoformat()}")
        
        # scraper
        scraper_response = scrapeLP.main({"url":url})
        if all([x is None for x in scraper_response.values()]):
            logging.error(f'unable to access website {url}')
            return func.HttpResponse(None)
        scraper_titles = scraper_response["title"]
        scraper_text = scraper_response["text"]
        logging.info('scrape landing page metadata done')

        # extract keywords
        keywords = getKw(scraper_text)
        keywords = [x[0] for x in keywords]
        logging.info(f'kw nana {keywords}')
        
        images_input = {
            "kw":   keywords, 
            "n":    config.n_images
        }

        titles_input = {
            "title":    scraper_titles, 
            "text":     scraper_text, 
            "kw":       keywords, 
            "n":        config.n_titles
        }
            
        category_input = {
            "title":    scraper_titles,
            "kw":       keywords
        }
        
        # async - images, titles, category
        results = await asyncio.gather(
            getImages.main(images_input),
            getTitles.main(titles_input),
            getCat.main(category_input)
        )
        images = results[0][0]
        shutterstock_dict = results[0][1] 
        titles = results[1]
        category = results[2]
        
        if config.google_lense["enabled"]:
           images = await imageScore(images, keywords) 
        
        ret_dict = {
            "url":                  url, 
            "titles":               titles["titles"], 
            "stitles":              titles["stitles"],
            "descriptions":         titles["descs"],
            "images":               images,
            "shutterstock_dict":    shutterstock_dict,
            "category":             category["category"],
            "kw":                   keywords,
            "createdDate":          tcd.isoformat(),
            "duration":             str(time.time()-t0),
            "version":              config.application_version
        }
        
        # db
        if config.sql["enabled"]:
            imagesDb = []
            titlesDb = []
            shutterstock_images = [image["image"] for image in shutterstock_dict]
            restImages = [image for image in images if (image not in shutterstock_images)]
            logging.info(f'shutter_stock {shutterstock_images} rest images {restImages}')
            for image in restImages:
                img = Image("testStock", image, None)
                imagesDb.append(img)
            for element in shutterstock_dict:
                img = Image("testStock", element["image"], stock_id=element["id"])
                imagesDb.append(img)
                
            for title in titles["titles"]:
                titlesDb.append(Title(title))
                
            dbUtils.insert_creative_data(imagesDb, titlesDb, keywords)

        return func.HttpResponse(json.dumps(ret_dict))