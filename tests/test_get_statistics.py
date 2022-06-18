import unittest
import azure.functions as func
import getStatistics
from json import dumps

test_url = "https://oqadgen2.azurewebsites.net/api/getStatistics"

class GetStatisticsTest(unittest.TestCase):

    async def test_get_statistics_valid_url(self):
        input_body = {
            "creatives":[
                {
                    "image": "https://image.shutterstock.com/z/stock-photo-front-end-loader-excavator-moves-along-the-road-in-a-stone-quarry-against-the-background-of-large-1962412129.jpg",
                    "title": "Web Player: The ultimate music experience for iOS users."
                },
                {
                    "image": "https://image.shutterstock.com/z/stock-photo-panorama-of-a-mining-plant-with-a-front-end-loader-transporting-crushed-stone-1954936822.jpg",
                    "title": "Web Player: The ultimate music experience for iOS users."
                }
            ],
            "landingPage": "https://open.spotify.com/"
        }
        test_request = func.HttpRequest(method="Post", url=test_url, body=dumps(input_body))
        test_response = await getStatistics.main(test_request)
        test_response_body = test_response.get_body()
        self.assertTrue(test_response.status_code < 400)
        self.assertTrue(len(test_response_body["creatives"]) > 0)
        self.assertTrue(test_response_body["creatives"]["Score"] > 0)

if __name__ == '__main__':
    unittest.main()
