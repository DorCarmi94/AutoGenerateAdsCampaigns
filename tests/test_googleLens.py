import unittest
from shared_code import GoogleLense
from shared_code.commonClasses import Configuration
from shared_code.utils import load_yaml

def make_order():
    order = {}
    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare

ordered,compare=make_order()
unittest.defaultTestLoader.sortTestMethodsUsing=compare

class GoogleTestCase(unittest.TestCase):
    def setUp(self):
        self.cfg = load_yaml("./creativesFromUrl/config.yaml")
        self.config = Configuration(self.cfg)
        self.conn=None

    async def test_imagesLables(self):
       labels= await GoogleLense.imagesLables(["https://images.pexels.com/photos/3764353/pexels-photo-3764353.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"])
       print(labels)
       self.assertTrue(len(labels)>0)

    async def test_empty(self):
       labels= await GoogleLense.imagesLables([])
       print(labels)
       self.assertTrue(len(labels)==0)

    async def test_wrongurl(self):
       labels= await GoogleLense.imagesLables(["ghjkl","fghjk"])
       print(labels)
       self.assertTrue(len(labels)==0)