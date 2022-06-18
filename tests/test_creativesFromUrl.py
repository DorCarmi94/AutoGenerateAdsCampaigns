import unittest
import azure.functions as func
import creativesFromUrl
from json import dumps

test_url = "https://oqadgen2.azurewebsites.net/api/creativesFromUrl"

class CreativesFromUrlTest(unittest.TestCase):

    async def test_ad_creator_valid_url(self):
        input_body = {"url": "https://www.hangoverweekends.co.uk/blog/the-top-10-most-popular-cocktails/"}
        test_request = func.HttpRequest(method="Post", url=test_url, body=dumps(input_body))
        test_response = await creativesFromUrl.main(test_request)
        test_response_body = test_response.get_body()
        self.assertTrue(test_response.status_code < 400)
        self.assertTrue(len(test_response_body["titles"]) > 0)
        self.assertTrue(len(test_response_body["category"]) > 0)
        self.assertTrue(len(test_response_body["kw"]) > 0)

    async def test_ad_creator_not_valid_url(self):
        input_body = {"url": "not valid url format"}
        test_request = func.HttpRequest(method="Post", url=test_url, body=dumps(input_body))
        test_response = await creativesFromUrl.main(test_request)
        test_response_body = test_response.get_body()
        self.assertTrue(test_response.status_code < 400)
        self.assertTrue(len(test_response_body["titles"]) == 0)
        self.assertTrue(len(test_response_body["category"]) == 0)
        self.assertTrue(len(test_response_body["kw"]) == 0)

    async def test_ad_creator_empty_url(self):
        input_body = {"url": ""}
        test_request = func.HttpRequest(method="Post", url=test_url, body=dumps(input_body))
        test_response = await creativesFromUrl.main(test_request)
        test_response_body = test_response.get_body()
        self.assertTrue(test_response.status_code < 400)
        self.assertTrue(len(test_response_body["titles"]) == 0)
        self.assertTrue(len(test_response_body["category"]) == 0)
        self.assertTrue(len(test_response_body["kw"]) == 0)

    async def test_ad_creator_duration_valid_url(self):
        input_body = {"url": "https://www.hangoverweekends.co.uk/blog/the-top-10-most-popular-cocktails/"}
        test_request = func.HttpRequest(method="Post", url=test_url, body=dumps(input_body))
        test_response = await creativesFromUrl.main(test_request)
        test_response_body = test_response.get_body()
        self.assertTrue(test_response_body["duration"] > 20)

    async def test_ad_creator_duration_not_valid_url(self):
        input_body = {"url": "not valid url format"}
        test_request = func.HttpRequest(method="Post", url=test_url, body=dumps(input_body))
        test_response = await creativesFromUrl.main(test_request)
        test_response_body = test_response.get_body()
        self.assertTrue(test_response_body["duration"] < 10)

    async def test_ad_creator_duration_empty_url(self):
        input_body = {"url": ""}
        test_request = func.HttpRequest(method="Post", url=test_url, body=dumps(input_body))
        test_response = await creativesFromUrl.main(test_request)
        test_response_body = test_response.get_body()
        self.assertTrue(test_response_body["duration"] < 10)

    async def test_ad_creator_missing_url(self):
        input_body = {}
        test_request = func.HttpRequest(method="Post", url=test_url, body=dumps(input_body))
        test_response = await creativesFromUrl.main(test_request)
        self.assertTrue(test_response.status_code < 400)

    async def test_ad_creator_duration_missing_url(self):
        input_body = {}
        test_request = func.HttpRequest(method="Post", url=test_url, body=dumps(input_body))
        test_response = await creativesFromUrl.main(test_request)
        test_response_body = test_response.get_body()
        self.assertTrue(test_response_body["duration"] < 10)


if __name__ == '__main__':
    unittest.main()
