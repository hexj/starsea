# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CubeItem(scrapy.Item):
    name = scrapy.Field()
    symbol = scrapy.Field()
    market = scrapy.Field()
    net_value = scrapy.Field()
    daily_gain = scrapy.Field()
    monthly_gain = scrapy.Field()
    total_gain = scrapy.Field()
    annualized_gain = scrapy.Field()
    closed_at = scrapy.Field()
    owner = scrapy.Field()


class OwnerItem(scrapy.Item):
    id = scrapy.Field()
    screen_name = scrapy.Field()
