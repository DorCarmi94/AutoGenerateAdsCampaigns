import unittest
import aiohttp
import shared_code.getImages as getImages

class MyTestCase(unittest.TestCase):
    async def test_pixabay_valid_result(self):
        kw = ['apple', 'banana', 'lemon']
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pixabay(session, kw, n)
            self.assertEqual(type(images), list)
    
    async def test_pixabay_result_length(self):
        kw = ['apple', 'banana', 'lemon']
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pixabay(session, kw, n)
            self.assertLessEqual(len(images), n)
    
    async def test_pixabay_single_kw(self): 
        kw = ['phone']
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pixabay(session, kw, n)
            self.assertGreaterEqual(len(images), 1)
            
    async def test_pixabay_empty_kw(self):
        kw = []
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pixabay(session, kw, n)
            self.assertEqual(images, [])
            
    async def test_pixabay_n_zero(self):
        kw = []
        n = 0
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pixabay(session, kw, n)
            self.assertEqual(images, [])
            
    async def test_shutterstock_valid_result(self):
        kw = ['apple', 'banana', 'lemon']
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_shutterstock(session, kw, n)
            self.assertEqual(type(images), list)
    
    async def test_shutterstock_result_length(self):
        kw = ['apple', 'banana', 'lemon']
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_shutterstock(session, kw, n)
            self.assertLessEqual(len(images), n)
    
    async def test_shutterstock_single_kw(self): 
        kw = ['phone']
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_shutterstock(session, kw, n)
            self.assertGreaterEqual(len(images), 1)
            
    async def test_shutterstock_empty_kw(self):
        kw = []
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_shutterstock(session, kw, n)
            self.assertEqual(images, [])
            
    async def test_shutterstock_n_zero(self):
        kw = []
        n = 0
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_shutterstock(session, kw, n)
            self.assertEqual(images, [])
            
    async def test_pexels_valid_result(self):
        kw = ['apple', 'banana', 'lemon']
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pexels(session, kw, n)
            self.assertEqual(type(images), list)
    
    async def test_pexels_result_length(self):
        kw = ['apple', 'banana', 'lemon']
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pexels(session, kw, n)
            self.assertLessEqual(len(images), n)
    
    async def test_pexels_single_kw(self): 
        kw = ['phone']
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pexels(session, kw, n)
            self.assertGreaterEqual(len(images), 1)
            
    async def test_pexels_empty_kw(self):
        kw = []
        n = 5
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pexels(session, kw, n)
            self.assertEqual(images, [])
            
    async def test_pexels_n_zero(self):
        kw = []
        n = 0
        with aiohttp.ClientSession() as session:
            images = await getImages.getImages_pexels(session, kw, n)
            self.assertEqual(images, [])
            
    async def test_mainScenario_valid_result(self):
        kw = ['apple', 'banana', 'lemon']
        n = 5
        data = {"kw":kw, "n":n, "stock":""}
        images = getImages.main(data)
        self.assertEqual(type(images), list)
        
    async def test_mainScenario_results_length(self):
        kw = ['apple', 'banana', 'lemon']
        n = 5
        data = {"kw":kw, "n":n, "stock":""}
        images = getImages.main(data)
        self.assertLessEqual(len(images), n*3)
        
    async def test_mainScenario_single_kw(self):
        kw = ['phone']
        n = 5
        data = {"kw":kw, "n":n, "stock":""}
        images = getImages.main(data)
        self.assertGreaterEqual(len(images), 3)
        
    async def test_mainScenario_empty_kw(self):
        kw = []
        n = 5
        data = {"kw":kw, "n":n, "stock":""}
        images = getImages.main(data)
        self.assertEqual(images, [])
        
    async def test_mainScenario_n_zero(self):
        kw = ['apple', 'banana', 'lemon']
        n = 0
        data = {"kw":kw, "n":n, "stock":""}
        images = getImages.main(data)
        self.assertEqual(images, [])


if __name__ == '__main__':
    unittest.main()
