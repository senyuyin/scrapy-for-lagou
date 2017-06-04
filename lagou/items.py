# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LagouItem(Item):

    secondType = Field()
    firstType = Field()
    companyFullName = Field()
    city = Field()
    workYear = Field()
    industryField = Field()
    salary = Field()
    positionName = Field()





