# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyappItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
  package_name = scrapy.Field() 
  display_name = scrapy.Field()
  rate_number = scrapy.Field()
  download_number = scrapy.Field()
  update_time = scrapy.Field()
  file_urls = scrapy.Field()
  _id = scrapy.Field()
  sha1 = scrapy.Field()


class QhItem(scrapy.Item):
  display_name = scrapy.Field()
  rate_number = scrapy.Field()
  download_number = scrapy.Field()
  file_urls = scrapy.Field()
  _id = scrapy.Field()
  sha1 = scrapy.Field()

class BaiduItem(scrapy.Item):
  package_name = scrapy.Field() 
  display_name = scrapy.Field()
  rate_number = scrapy.Field()
  download_number = scrapy.Field()
  file_urls = scrapy.Field()
  _id = scrapy.Field()
  sha1 = scrapy.Field()

