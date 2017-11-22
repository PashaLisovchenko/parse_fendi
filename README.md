## Web crawler

Web crawler for [Fendi](https://www.fendi.com)

## Install

``` bash
$ python3 -m venv env_name
$ . env_name/bin/activate
$ pip install -r requirements.txt
```
## PostgreSQL
``` bash
$ sudo apt-get install postgresql postgresql-server-dev-9.5

Open the PostgreSQL console
$ sudo -u postgres psql postgres

Create user
$ create user user_name with password 'password';
$ alter role user_name set client_encoding to 'utf8';
$ alter role user_name set default_transaction_isolation to 'read committed';
$ alter role user_name set timezone to 'UTC';

Create a base for our project
$ create database scrapy_fendi owner user_name;

Exit the console
$ \q

And now we go to the database in our created user
$ sudo -U user_name -h localhost -d scrapy_fendi

Now need create two tables (product and price)
CREATE TABLE price (
  pk          SERIAL NOT NULL PRIMARY KEY,
  product_id  VARCHAR(80),
  price       VARCHAR(15),
  color       VARCHAR(500),
  size        VARCHAR(400),
  stock_level VARCHAR(25),
  currency    VARCHAR(10),
  date        VARCHAR(30)
);
CREATE TABLE product (
  pk          SERIAL NOT NULL PRIMARY KEY,
  id          VARCHAR(80),
  name        VARCHAR(80),
  brand       VARCHAR(10),
  description VARCHAR(800),
  made_in     VARCHAR(20),
  materials   VARCHAR(200),
  images      VARCHAR(1000),
  url         VARCHAR(80),
  site        VARCHAR(50),
  categories  VARCHAR(100)
);
```

## Usage
```
In the project to connect to the created database
self.connection = psycopg2.connect(host='localhost', database='scrapy_fendi', user='pasha', password='123')
```

``` bash
$ scrapy crawl fendi -a url='https://www.fendi.com/us/man/'
$ scrapy crawl fendi -a url='https://www.fendi.com/us/woman/'
```
