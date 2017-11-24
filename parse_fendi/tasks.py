import psycopg2
from celery import Celery

app = Celery(broker='redis://localhost:6379//', backend='redis://')


@app.task
def save_product_db(item):
    connection = psycopg2.connect(host='localhost', database='scrapy_fendi', user='pasha', password='123')
    cursor = connection.cursor()
    print('*' * 50)
    print("product")
    keys = item.keys()
    columns = ','.join(keys)
    values = ','.join(['%({})s'.format(k) for k in keys])
    insert = 'insert into product ({0}) values ({1})'.format(columns, values)

    cursor.execute(insert, item)
    connection.commit()


@app.task
def save_price_db(item):
    print('*' * 50)
    print("price")
    connection = psycopg2.connect(host='localhost', database='scrapy_fendi', user='pasha', password='123')
    cursor = connection.cursor()
    dict_params = item.get('params')
    price = dict_params['price']
    color = ','.join(dict_params['color'])
    size = ','.join(dict_params['size'])

    sql = """INSERT INTO price(product_id, price, color, size, stock_level, currency, date)
          VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    data = (item.get('product_id'), price, color, size, item.get('stock_level'),
            item.get('currency'),item.get('date'))

    cursor.execute(sql, data)
    connection.commit()


if __name__ == '__main__':
    app.worker_main()
