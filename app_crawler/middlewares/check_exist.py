from scrapy.exceptions import DropItem


class CheckExist(object):

  def process_spider_input(self, response, spider):
    print 'check exist'
    collection = spider.get_collection()
    cond = {'parse_url': response.url}
    if collection.find_one(cond) is not None:
      print 'duplicate request'
      raise DropItem('duplicate request')
    else:
      return None
