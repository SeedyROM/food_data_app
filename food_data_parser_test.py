import os
import glob
import unittest
import pprint

from food_data_parser import FoodDataParser


FOOD_DATA_PATH = '/home/breath/Downloads/food_data/'
FOOD_DATA_GLOB = os.path.join(FOOD_DATA_PATH, '*.xlsx')

class TestFoodDataParser(unittest.TestCase):

    def setUp(self):
        self.food_data_files = glob.glob(FOOD_DATA_GLOB)
        self.foo_data = self.food_data_files[0]

        self.parser = FoodDataParser()
        self.data = self.parser(self.foo_data)

    def test_parses_all_data(self):
        for filename in self.food_data_files:

            data = self.parser(filename)
            variants_count = len(data['variants'])

            self.assertTrue(variants_count > 0)

    def test_creates_proper_data_structure(self):
        self.assertTrue({'name', 'variants', 'sources'} == self.data.keys())

    def test_parses_name(self):
        data = self.parser(FOOD_DATA_PATH + 'apples.xlsx')
        self.assertTrue(data['name'].casefold() == 'apples')
