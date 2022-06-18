from distutils.command.config import config
import openai
from shared_code.utils import load_yaml
from shared_code.commonClasses import Configuration

cfg = load_yaml("creativesFromUrl/config.yaml")
config = Configuration(cfg)

openai.organization = config.openai["company"]
openai.api_key = config.openai["OPENAI_API_KEY"]
FINE_TUNED_MODEL = config.openai["cat_model"]

async def main(req_body):
    title = req_body["title"]
    p = req_body["kw"]
    YOUR_PROMPT = f"keywords: {' '.join(p)}\ntitle: {title}\n\n###\n\n"
    ans = openai.Completion.create(
      model=FINE_TUNED_MODEL,
      prompt=YOUR_PROMPT)
    cat = ans.to_dict()["choices"][0]["text"].split("END")[0]

    return {"category":cat}