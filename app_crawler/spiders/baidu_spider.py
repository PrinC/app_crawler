import scrapy
import urlparse
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from app_crawler.items import BaiduItem
from app_crawler.service.mongoable import Mongoable


class BaiduSpider(Mongoable, CrawlSpider):
  name = "baidu"
  start_urls = ["http://shouji.baidu.com/software/"]

  rules = (Rule(LinkExtractor()))
  rules = (Rule(LinkExtractor(allow=('\/software\/item'),),follow=True, callback='parse_item'),)

  def __init__(self, **kwargs):
    Mongoable.__init__(self, **kwargs)
    CrawlSpider.__init__(self, **kwargs)
    self.start()

  def get_collection(self):
    return self.collection

  def parse_item(self, response):
    item = BaiduItem()
    item['parse_url'] = response.url
    item['file_urls'] = response.selector.css('.area-download .apk').xpath('@href').extract()
    if urlparse.urlparse(item['file_urls'][0]).netloc != 'p.gdown.baidu.com':
      return
    item['display_name'] = response.selector.css('.app-name span::text').extract()[0]
    item['rate_number'] = str(int(response.selector.css('.star-percent').xpath('@style').extract()[0][6:-1])/10.0)
    item['download_number'] = response.selector.css('.detail .download-num::text').extract()[0][5:]
    return item

  def closed(self):
    super(Mongoable, self).close()
