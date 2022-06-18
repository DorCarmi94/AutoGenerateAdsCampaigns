import unittest
from shared_code import dbUtils
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

class DBWriterTestCase(unittest.TestCase):
    ID_IDX = 0
    IMAGE_URL_IDX = 2
    TITLE_URL_IDX = 1

    STAT_IMAGE_IDX=1
    STAT_TITLE_IDX=2

    KEYWORD_IDX=1
    KEYWORD_IMAGE_IDX=2
    KEYWORD_TITLE_IDX=3

    def setUp(self):
        self.cfg = load_yaml("./creativesFromUrl/config.yaml")
        self.config = Configuration(self.cfg)
        self.conn=None

    @ordered
    def test_a_open_connetion(self):
        try:
            self.conn=dbUtils.open_connection()
            self.assertIsNotNone(self.conn)
        except :
            self.fail("Bad opening connection")

    @ordered
    def test_b_close_connetion(self):
        try:
            self.conn = dbUtils.open_connection()
            dbUtils.close_connection(self.conn)
        except:
            self.fail("Bad closing connection")


    def checkImageUrlExists(self,url,id=None):
        res_imgs = dbUtils.get_resources(self.conn, self.config.sql["images_table_name"])
        urls = [(res[self.IMAGE_URL_IDX],res[self.ID_IDX]) for res in res_imgs]
        urls_set = dict(urls)
        if(id is None):
            return url in urls_set
        else:
            return (url in urls_set)  and urls_set[url]==id


    def checkTitleExists(self,title,id=None):
        res_imgs = dbUtils.get_resources(self.conn, self.config.sql["titles_table_name"])
        titles = [(res[self.TITLE_URL_IDX],res[self.ID_IDX]) for res in res_imgs]
        titles_set = dict(titles)
        if(id is None):
            return title in titles_set
        else:
            return (title in titles_set)  and titles_set[title]==id

    def checkStatExists(self,image_id,title_id,id=None):
        res_stats = dbUtils.get_statistics_by_imageId_titleId(self.conn, image_id, title_id)
        return res_stats != None

    def checkKeywordExists(self,image_id,title_id,keyword,id=None):
        res_stats = dbUtils.get_resources(self.conn, self.config.sql["keywords_table_name"])
        statIds=[x[self.ID_IDX] for x in res_stats
                 if x[self.KEYWORD_IMAGE_IDX]==image_id and x[self.KEYWORD_TITLE_IDX]==title_id
                 and x[self.KEYWORD_IDX]==keyword]
        if(len(statIds)<=0):
            return False
        else:
            return id in statIds

    def getTitleID(self,title):
        res_imgs = dbUtils.get_resources(self.conn, self.config.sql["titles_table_name"])
        titles = [(res[self.TITLE_URL_IDX],res[self.ID_IDX]) for res in res_imgs]
        titles_set = dict(titles)
        if title in titles_set:
            return titles_set[title]
        else:
            return "-1"

    def getImageID(self,url):
        res_imgs = dbUtils.get_resources(self.conn, self.config.sql["images_table_name"])
        urls = [(res[self.IMAGE_URL_IDX],res[self.ID_IDX]) for res in res_imgs]
        urls_set = dict(urls)
        if url in urls_set:
            return urls_set[url]
        else:
            return "-1"

    def getStatisticID(self,title,url):
        res_imgs = dbUtils.get_resources(self.conn, self.config.sql["statistics_table_name"])
        urls = [(res[self.IMAGE_URL_IDX],res[self.ID_IDX]) for res in res_imgs]
        urls_set = dict(urls)
        if url in urls_set:
            return urls_set[url]
        else:
            return "-1"

    @ordered
    def test_c_insert_image(self):
        try:
            self.conn=dbUtils.open_connection()
            test_url="test_image_url"
            while(self.checkImageUrlExists(test_url)):
                test_url+="1"
            id=dbUtils.insert_image(self.conn,"test_stok",test_url)
            self.assertTrue(self.checkImageUrlExists(test_url,id))
            dbUtils.close_connection(self.conn)
        except Exception as ex:
            self.fail(ex)

    @ordered
    def test_d_get_resource_by_id(self):
        self.conn = dbUtils.open_connection()
        test_url = "test_image_url"
        while (self.checkImageUrlExists(test_url)):
            test_url += "1"
        id = dbUtils.insert_image(self.conn, "test_stock", test_url)
        result=dbUtils.get_resource_by_id(self.conn,self.config.sql["images_table_name"],id)
        self.assertTrue(len(result)>0)

    @ordered
    def test_e_insert_title(self):
        try:
            self.conn = dbUtils.open_connection()
            test_title = "test_title"
            while (self.checkTitleExists(test_title)):
                test_title += "1"
            id = dbUtils.insert_title(self.conn, test_title)
            self.assertTrue(self.checkTitleExists(test_title, id))
            dbUtils.close_connection(self.conn)
        except Exception as ex:
            self.fail(ex)


    def test_insert_statistics(self):
        try:
            self.conn = dbUtils.open_connection()
            test_title = "test_title"
            imageID=""
            titleID=""
            if (not self.checkTitleExists(test_title)):
                titleID=dbUtils.insert_title(self.conn,test_title)
            else:
                titleID=self.getTitleID(test_title)
            test_url = "test_image_url"
            if(not self.checkImageUrlExists(test_url)):
                imageID=dbUtils.insert_image(self.conn,test_url)
            else:
                imageID=self.getImageID(test_url)

            stat_id=dbUtils.insert_statistics(self.conn,imageID,titleID,50,50,50)
            self.assertTrue(self.checkStatExists(imageID,titleID,stat_id))
            dbUtils.close_connection(self.conn)
        except Exception as ex:
            self.fail(ex)

    def test_insert_keyword(self):
        try:
            self.conn = dbUtils.open_connection()
            test_title = "test_title"
            imageID = ""
            titleID = ""
            if (not self.checkTitleExists(test_title)):
                titleID = dbUtils.insert_title(self.conn, test_title)
            else:
                titleID = self.getTitleID(test_title)
            test_url = "test_image_url"
            if (not self.checkImageUrlExists(test_url)):
                imageID = dbUtils.insert_image(self.conn, test_url)
            else:
                imageID = self.getImageID(test_url)

            test_keyword="test"

            keyword_id = dbUtils.insert_keyword(self.conn, test_keyword,imageID,titleID)
            self.assertTrue(self.checkKeywordExists(imageID, titleID,test_keyword, keyword_id))
            dbUtils.close_connection(self.conn)
        except Exception as ex:
            self.fail(ex)







