import logging
from shared_code.GoogleLense import imagesLables

async def imageScore(images, keywords):
    #calculating image score:
    imageData = await imagesLables(images)
    logging.info(f'images data {imageData}')
    images = imageData.keys()
    image_score = {}
    for image in images:
        lables = [list(x) for x in zip(*imageData[image])][0]
        scores = [list(x) for x in zip(*imageData[image])][1]
        score = 0
        for pos in range(len(lables)):
            if lables[pos].lower() in keywords:
                score += scores[pos]
        image_score[image] = score
    sorted_images = sorted(image_score.keys(), key=image_score.get, reverse= True)

    return sorted_images
    

        
        