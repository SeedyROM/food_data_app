import unittest
import re
import json

from food_data_scraper import FoodDataScraper


class TestFoodDataScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = FoodDataScraper()

    def test_gets_raw_html(self):
        self.assertTrue('html' in self.scraper.get_raw_html())

    def test_gets_html(self):
        self.assertTrue(hasattr(self.scraper.get_html(), 'body'))

    def test_gets_data_hrefs(self):
        for xlsx_url in self.scraper.get_xlsx_urls():
            self.assertIsNotNone(re.search(r'\.xls[x]?', xlsx_url))

    def test_gets_xlsx_data(self):
        data = self.scraper.get_xlsx_data(self.scraper.urls[0])
        self.assertTrue(data['name'] == 'Apples')

    # @FoodDataScraper.for_parsed_files
    # def test_scraper_decorator(self, food_item):
    #     with open('x.log', 'a') as log:
    #         log.write(json.dumps(food_item))
