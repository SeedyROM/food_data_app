import json

from pprint import pprint

from food_data_scraper import FoodDataScraper

class Example:

    def __init__(self):
        self.food_data = []

    @FoodDataScraper.for_parsed_files
    def do_something(self, parsed_data):
        self.food_data.append(parsed_data)

    def write_data(self, file_name='food_data.json'):
        with open(file_name, 'w+') as data_file:
            data_file.write(json.dumps({
                'food_data': self.food_data
            }))

if __name__ == '__main__':
    e = Example()
    e.do_something()
    e.write_data()
