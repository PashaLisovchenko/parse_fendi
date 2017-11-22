import psycopg2
from celery import Celery, shared_task
from parse_fendi.items import Product, Price

app = Celery()
app.conf.broker_url = 'redis://'
app.conf.result_backend = 'redis://'


@app.task()
def save_db(item, connection, cursor):

    print('*'*50)
    try:
        if type(item) is Product:
            keys = item.keys()
            columns = ','.join(keys)
            values = ','.join(['%({})s'.format(k) for k in keys])
            insert = 'insert into product ({0}) values ({1})'.format(columns, values)

            cursor.execute(insert, item)
            connection.commit()
            cursor.fetchall()

        elif type(item) is Price:
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
            cursor.fetchall()

    except psycopg2.DatabaseError as e:
        connection.commit()
        print("Error: %s" % e)

    return item
