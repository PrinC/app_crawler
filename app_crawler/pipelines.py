# -*- coding: utf-8 -*-
import hashlib
import os
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

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
    path = os.path.join(self.filestore, path)
    try:
      with open(path) as f:
        content = f.read()
    except IOError as e:
      print result, e.message
      raise DropItem("open error")
    sha1obj = hashlib.sha1()
    sha1obj.update(content)
    id = sha1obj.hexdigest()
    item['_id'] = id
    item['sha1'] = id
    item['file_url'] = item['file_urls'][0]
    del item['file_urls'] 
    try: 
      os.rename(path, os.path.join(os.path.dirname(path), id)) 
    except OSError as e:
      raise DropItem("Cannot rename apk file to sha1")
    return item

  def open_spider(self, spider):
    self.filestore = spider.settings.get('FILES_STORE')
    super(ApkCrawlerFilesPipeline, self).open_spider(spider)

'''
class CheckExistPipeline(object):
  def process_item(self, item, spider):
    print 'checkexist pipeline'

    filter = {}
    if 'package_name' not in item:
      filter["parse_url"] = item["parse_url"]
    else:
      filter["package_name"] = item["package_name"]
    if self._collection.find_one(filter) is not None:
      print 'duplicate request'
      raise DropItem('duplicate request')
    else:
      return item

  def open_spider(self, spider):
    self._collection = spider.get_collection()
'''

class MongoPipeline(object):

  def open_spider(self, spider):
    self._collection = spider.get_collection()

  def process_item(self, item, spider):
    if 'file_url' not in item:
      item['file_url'] = item['file_urls'][0]
    if '_id' not in item:
      sha1obj = hashlib.sha1()
      sha1obj.update(item['display_name'].encode('utf-8'))
      id = sha1obj.hexdigest()
      item['_id'] = id
    try:
      self._collection.insert(item)
    except:
      raise DropItem('Mongo Error')
    return item
