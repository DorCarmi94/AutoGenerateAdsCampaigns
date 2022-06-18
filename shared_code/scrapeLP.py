import logging
import nltk 
from newspaper import Article

nltk.download('punkt') 

def main(req_body):
    logging.info('scraper start')
    url = req_body['url']
    print(f"input: {url}")
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    ret_dict = {
      "text":article.text, 
      "title":article.title,
      "desc":article.meta_description, 
      "kw_article":article.keywords,
      "summary":article.summary,
      }
    if "Attention Required! | Cloudflare" in ret_dict["text"]:
      ret_dict = {k:None for k in ret_dict.keys()}
      
    return ret_dict
