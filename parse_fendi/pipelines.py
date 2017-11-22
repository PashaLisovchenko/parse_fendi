import psycopg2
# from parse_fendi.items import Product, Price
from parse_fendi.task import save_db


class ParseFendiPipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(host='localhost', database='scrapy_fendi', user='pasha', password='123')
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        return save_db(item, self.connection, self.cursor)
