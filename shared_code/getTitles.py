import logging
import openai
from shared_code.utils import load_yaml
from shared_code.commonClasses import Configuration

cfg = load_yaml("creativesFromUrl/config.yaml")
config = Configuration(cfg)

openai.organization = config.openai["company"]
openai.api_key = config.openai["OPENAI_API_KEY"]
FINE_TUNED_MODEL = config.openai["titles_model"]

async def main(req_body):
    logging.info(f'titles generation service {req_body}')
    title = req_body["title"]
    p = req_body["kw"]
   
    TITLE_PROMPT=f"Write a catchy creative ad title in one line from the following keywords set and header:\n\nkeywords: {' '.join(p)}\nheader: {title}\n"
    print(f"PROMPT: {TITLE_PROMPT}")
    titles = []
    stitles = []
    descs = []
    for i in range(cfg["n_titles"]):
        ans = openai.Completion.create(
                engine="text-davinci-002",
                prompt=TITLE_PROMPT,
                temperature=0.5,
                max_tokens=120,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
        title = ans.to_dict()["choices"][0]["text"][1:].split("\n")[0]
        if title in titles:
            continue

        titles.append(title)
        # now subtitles subtitle:
        STITLE_PROMPT=f"""generate subtitle to the following title: "{title}" """
        ans = openai.Completion.create(
                engine="text-davinci-002",
                prompt=STITLE_PROMPT,
                temperature=0.5,
                max_tokens=120,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
        print(f"stitle answer: {ans.to_dict()}")
        stitle = ans.to_dict()["choices"][0]["text"][1:].split("\n")[-1]
        stitles.append(stitle)
        
        # now description subtitle:
        DESC_PROMPT=f"""generate blog content summary to the following title: "{title}" """
        ans = openai.Completion.create(
                engine="text-davinci-002",
                prompt=DESC_PROMPT,
                temperature=0.5,
                max_tokens=120,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
        desc = ans.to_dict()["choices"][0]["text"][1:].split("\n")[-1]
        descs.append(desc)

        logging.info(f"{i}: {title} | {stitle} | {desc}")

    return {
        "titles": list(set(titles)), 
        "stitles": list(set(stitles)), 
        "descs": list(set(descs))
    }

