# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CubeItem(scrapy.Item):
    symbol = scrapy.Field()
    data_item = scrapy.Field()


class CubeRebalanceItem(scrapy.Item):
    symbol = scrapy.Field()
    data_list = scrapy.Field()


class CubeRebalanceHistoryItem(scrapy.Item):
    symbol = scrapy.Field()
    data_list = scrapy.Field()


class CubeProfitItem(scrapy.Item):
    symbol = scrapy.Field()
    data_list = scrapy.Field()


class OwnerItem(scrapy.Item):
    id = scrapy.Field()
    screen_name = scrapy.Field()
