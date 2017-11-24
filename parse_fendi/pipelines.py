from .tasks import save_price_db, save_product_db
from .items import Product, Price


class ParseFendiPipeline(object):
    def __init__(self):
        self.store = list()

    def save_items(self):
        for store_item in self.store:
            if isinstance(store_item, Product):
                save_product_db.delay(dict(store_item))
            elif isinstance(store_item, Price):
                save_price_db.delay(dict(store_item))
        self.store.clear()

    def process_item(self, item, spider):
        self.store.append(item)
        if len(self.store) > 100:
            self.save_items()
        return item

    def close_spider(self, spider):
        self.store and self.save_items()
