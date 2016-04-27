# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    uri = scrapy.Field()
    name = scrapy.Field()
    gross = scrapy.Field()

    rating = scrapy.Field()
    desc = scrapy.Field()
    duration = scrapy.Field()
    rating = scrapy.Field()
    credit = scrapy.Field()
    genre = scrapy.Field()
    pass
