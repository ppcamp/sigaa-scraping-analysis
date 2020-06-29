# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SigaaItem(scrapy.Item):
    # define the fields for your item here like:
    StartYearPeriod = scrapy.Field()
    CurrentYearPeriod = scrapy.Field()
    RA = scrapy.Field()
    Grid = scrapy.Field()
    CourseName = scrapy.Field()
    Semester = scrapy.Field()