import logging, json
import azure.functions as func
from shared_code.utils import load_yaml
from shared_code.commonClasses import Configuration
from shared_code import dbUtils
from random import randint

try:
    cfg = load_yaml("./creativesFromUrl/config.yaml")
except:
    cfg = load_yaml("../creativesFromUrl/config.yaml")

config = Configuration(cfg)

def evaluate_score(CTR, CPM):
    score = (CTR + CPM) / (2 * config.statistics["stats_max_value"]) * 100

    return score

def get_statistics_from_taboola(creativeId):
    pass

def generate_statistics(imageId, titleId):
    is_demo = config.statistics["demo_generate_stats"]
    if is_demo:
        stats_max_value = config.statistics["stats_max_value"]
        CTR = randint(0, stats_max_value)
        CPM = randint(0, stats_max_value)
        Score = evaluate_score(CTR, CPM)
        return CTR, CPM, Score
    else:
        return get_statistics_from_taboola(imageId + titleId)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('statistics function endpoint')
    req_body = req.get_json()
    try:
        creatives = req_body["creatives"]
        landing_page = req_body["landingPage"]    
    except:
        return func.HttpResponse("1 Request payload is not valid.", status_code=400)
    
    ret_creatives = []
    conn = dbUtils.open_connection()
    for creative in creatives:
        try:
            image_url = creative["image"]
            title_desc = creative["title"]
        except:
            return func.HttpResponse("2 Request payload is not valid.", status_code=400)
        image = dbUtils.get_image_by_url(conn, image_url)
        title = dbUtils.get_title_by_description(conn, title_desc)
        imageId = image[0]
        titleId = title[0]
        CTR, CPM, Score = generate_statistics(imageId, titleId)
        creative["CTR"], creative["CPM"], creative["Score"] = CTR, CPM, Score
        dbUtils.insert_statistics(conn, imageId=imageId, titleId=titleId, ctr=CTR, cpm=CPM, score=Score)
        ret_creatives.append(creative)
    
    ret_dict = {
            "creatives":            ret_creatives, 
            "landindPage":          landing_page
        }

    dbUtils.close_connection(conn)
    return func.HttpResponse(json.dumps(ret_dict))