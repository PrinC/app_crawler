# -*- coding: utf-8 -*-
import scrapy
import hashlib
import os
import pymongo
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from settings import *

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ApkCrawlerFilesPipeline(FilesPipeline):

  def item_completed(self, results, item, info):
    # read file, compute sha1, set id, rename file
    ok, result = results[0]
    if not ok:
      raise DropItem("Download apk failed")
    path = result['path']
    path = os.path.join(FILES_STORE, path)
    with open(path) as f:
      content = f.read()
    sha1obj = hashlib.sha1()
    sha1obj.update(content)
    id = sha1obj.hexdigest()
    item['_id'] = id
    item['sha1'] = id
    try: 
      os.rename(path, os.path.join(os.path.dirname(path), id)) 
    except OSError as e:
      raise DropItem("Cannot rename apk file to sha1")
    return item

class MongoPipeline(object):

  def __init__(self, mongo_uri, mongo_db, collection_name):
    self.mongo_uri = mongo_uri
    self.mongo_db = mongo_db
    self.collection_name = collection_name + '_meta'


  @classmethod
  def from_crawler(cls, crawler):
    return cls(
      mongo_uri = crawler.settings.get('MONGO_URI'),
      mongo_db = crawler.settings.get('MONGO_DATABASE', 'items'),
      collection_name = crawler.spider.name
    )

  def open_spider(self, spider):
    self.client = pymongo.MongoClient(self.mongo_uri)
    self.db = self.client[self.mongo_db]

  def close_spider(self, spider):
    self.client.close()

  def process_item(self, item, spider):
    self.db[self.collection_name].replace_one({'_id': item['_id']}, dict(item), upsert=True)
    return item