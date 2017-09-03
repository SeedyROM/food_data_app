import re
import xlrd
import glob

from pprint import pprint

def addendum_regex():
    addendum_pattern = r'^([0-9]+)(.+)'
    return re.compile(addendum_pattern)

def get_valid_cell_rows(data, cell_cursor=3):
    while not addendum_regex().match(data.cell_value(rowx=cell_cursor, colx=0)): # "USDA" not in data.cell_value(rowx=cell_cursor, colx=0):
        if cell_cursor > data.nrows: break
        yield (cell_cursor, data.cell_value(rowx=cell_cursor, colx=0))
        cell_cursor += 1

def get_addendum_by_id(data, addendum_id):
    addendum_start = None
    for row, _ in get_valid_cell_rows(data): addendum_start = row

    addendum = addendum_regex()

    cell_cursor = addendum_start + 1
    while cell_cursor < data.nrows:
        cell_data = data.cell_value(rowx=cell_cursor, colx=0)
        match = addendum.match(cell_data)
        if match:
            if int(match.groups()[0]) == addendum_id:
                return match.groups()[1]

        cell_cursor += 1


def get_data_columns(data, row):
    row = data.row(row)[1:]

    data = dict()
    data['avg_retail_price'] = (row[0].value, row[1].value.strip())
    data['prep_yield_factor'] = row[2].value
    data['size_of_cup_eq'] = (row[3].value, row[4].value)
    data['avg_price_per_cup'] = row[5].value

    return data

def get_food_variants(data):
    sub_column_name = None
    for row, first_column in get_valid_cell_rows(data):
        cell_pattern = r'([\w ]+)([0-9]+)$'
        column_data = re.compile(cell_pattern).match(first_column)

        if column_data is None and not data.cell_value(rowx=row, colx=1):
            sub_column_name = first_column
            continue
        elif column_data is None:
            continue

        column_info = column_data.groups()
        column_data = get_data_columns(data, row)
        column_data['storage_type'] = column_info[0] if not sub_column_name else f'{sub_column_name}: {column_info[0]}'

        addendum_id = int(column_info[1])
        column_data['addendum'] = get_addendum_by_id(data, addendum_id)

        yield column_data

def get_food_data(xlsx_file):
    data = xlrd.open_workbook(xlsx_file)
    data = data.sheet_by_index(0)

    food_data = dict()
    food_data['name'] = data.name
    food_data['variants'] = list(get_food_variants(data))

    for row in data.col(0):
        sources = re.compile(r'Source: (.+)').match(row.value)
        if sources:
            food_data['sources'] = sources.groups()[0]

    return food_data

for filename in glob.glob('/home/breath/Downloads/food_data/*.xlsx'):
    pprint(get_food_data(filename))
