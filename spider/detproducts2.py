# -*- coding: utf-8 -*-
import scrapy
import ast
import re

class DetproductsSpider(scrapy.Spider):
    name = 'detproducts'
    #Use only wishlist data
    start_urls = ['https://www.amazon.com/hz/wishlist/ls/2TMOBFVZQDJLZ']

    def parse(self, response):
        urls = response.css('h3.a-size-base a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)
        # Follow pagination link
        next_page_url = response.css('a.next::attr(href)').extract_first()
        if next_page_url :
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self,response):
        self.log('I just visited: ' + response.url)

        yield{
            'brand': response.css('div#bylineInfo_feature_div a::text').extract_first(),
            'name': response.css('span#productTitle::text').extract_first().lstrip().rstrip(),
            'url': response.url ,
            'before_price': response.css('div#price span.a-text-strike::text').extract_first(),
            'price': response.css('span#priceblock_ourprice::text').extract_first(),
            'color': response.css('div#variation_color_name span::text').extract_first().lstrip().rstrip(),
            'short_description': response.css('div#feature-bullets ul').extract_first().replace('"', ''),
            'description': response.css('div#dpx-aplus-product-description_feature_div').extract_first() ,
            'SKU': response.url,
            #'stock': response.css('p.stock::text').extract_first().split(' ', 1)[0],
            'img_urls': re.findall('"hiRes":(.+?),', response.xpath('//*[@id="imageBlock_feature_div"]/script/text()').extract_first(), re.S),
            #'img_urls': ast.literal_eval(response.css('div#imgTagWrapperId img::attr(data-a-dynamic-image)').extract_first().encode('ascii','ignore')).keys(),
            #'img_url2': response.css('div.product-main div.woocommerce-product-gallery__image a::attr(href)').extract()[1],
            #'img_url3': response.css('div.product-main div.woocommerce-product-gallery__image a::attr(href)').extract()[2],
            #'img_url4': response.css('div.product-main div.woocommerce-product-gallery__image a::attr(href)').extract()[3]

        }
