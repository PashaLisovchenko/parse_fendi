import scrapy
import datetime
from parse_fendi.items import Product, Price
SITE = "https://www.fendi.com"


class FendiSpider(scrapy.Spider):
    name = 'fendi'

    def __init__(self, url='https://www.fendi.com/us/man/', *args, **kwargs):
        super(FendiSpider, self).__init__(*args, **kwargs)
        self.url = url

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        if 'man' in response.url.split('/'):
            category_href = response.xpath("//div[@id='man-popover']/div[@class='subcategories']"
                                           "/div[contains(@class, 'two-cols')]/div[contains(@class, 'exp')]"
                                           "/ul[contains(@class, 'expandable-xs')]/li[contains(@class, ' ')]"
                                           "/a/@href").extract()

            category_full_url = [SITE+href for href in category_href][0:-1]
            # print(category_full_url)
            for url in category_full_url:
                yield scrapy.Request(url=url, callback=self.parse_item)
        elif 'woman' in response.url.split('/'):
            category_href = response.xpath("//div[@id='woman-popover']/div[@class='subcategories']"
                                           "/div[contains(@class, 'two-cols')]/div[contains(@class, 'exp')]"
                                           "/ul[contains(@class, 'expandable-xs')]/li[contains(@class, ' ')]"
                                           "/a/@href").extract()

            category_full_url = [SITE + href for href in category_href][0:-1]
            # print(category_full_url)
            for url in category_full_url:
                yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        item_href = response.xpath('//div[contains(@class,"product-card")]/div[@class="inner"]/figure/a/@href').extract()
        item_full_url = [SITE + href for href in item_href]
        # print(item_full_url)
        for url in item_full_url:
            yield scrapy.Request(url=url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        product = Product()
        price = Price()
        product['id'] = response.xpath("//div[@class='product-info']/div[@class='product-description']/p[@class='code']"
                                       "/span/text()").extract()[0]
        product['name'] = response.xpath("//div[@class='product-info']/div[@class='product-description']/h1"
                                         "/text()").extract()[0]
        product['brand'] = 'Fendi'
        product['description'] = ''.join(response.xpath("//div[@class='tab-content']/div[contains(@class, 'tab-pane')]"
                                                        "/p/text()").extract()[0])
        made_in = response.xpath("//div[@class='tab-content']/div[contains(@class, 'tab-pane')]/p"
                                 "/text()").extract()
        if len(made_in) > 1:
            product['made_in'] = made_in[1].strip()
        else:
            product['made_in'] = 'Made in Italy'

        product['categories'] = ','.join([response.xpath("//div[@class='breadcrumbs']/section[@class='breadcrumb']"
                                                         "/a[@class='main-area']/text()").extract()[0],
                                         response.xpath("//div[@class='breadcrumbs']/section[@class='breadcrumb']"
                                                        "/div[@class='dropdown']/button[@id='dropdown-main-category']"
                                                        "/text()").extract()[0]
                                         ])
        materials = response.xpath("//div[@class='tab-content']/div[contains(@class, 'tab-pane')]/ul/li[2]"
                                   "/span/text()").extract()
        if len(materials) != 0:
            product['materials'] = materials[0]
        else:
            product['materials'] = ''

        product['images'] = ','.join(response.xpath("//div[contains(@class, 'carousel-nav')]/div"
                                                    "/img/@data-src").extract())
        product['url'] = response.url
        product['site'] = SITE
        price['product_id'] = response.xpath("//div[@class='product-info']/div[@class='product-description']"
                                             "/p[@class='code']/span/text()").extract()[0]
        price_params = dict()

        price_params['price'] = response.xpath("//div[@class='product-info']/div[@class='product-description']"
                                               "/div[contains(@class, 'prices')]/span[@class='price ']"
                                               "/text()").extract()[0].strip()
        price_params['color'] = response.xpath("//div[@class='product-variant']/a/img/@alt").extract()

        price_params['size'] = [size.replace('\n', '').strip()
                                for size in response.xpath("//div[@class='form-group']/select"
                                                           "/option[@data-sold-out='false']//text()").extract()]
        price['params'] = price_params
        stock = response.xpath("//div[contains(@class,'product-form')]/form/span[@class='message']/text()").extract()
        if len(stock) != 0:
            price['stock_level'] = stock[0].strip()
        else:
            price['stock_level'] = 'Available'
        price['currency'] = 'USD'
        price['date'] = str(datetime.datetime.now())

        yield product
        yield price
