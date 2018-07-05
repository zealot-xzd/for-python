# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    phone = scrapy.Field()
    rent_money = scrapy.Field()
    rent_type = scrapy.Field()
    base_info = scrapy.Field()
