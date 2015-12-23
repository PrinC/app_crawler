import scrapy
import urlparse
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from app_crawler.items import QhItem

class QhSpider(CrawlSpider):
  name = "qh"
  allowed_domains = ["360.cn"]
  start_urls = ["http://zhushou.360.cn/list/index/cid/1"]
  rules = (Rule(LinkExtractor(allow=('detail\/index\/soft_id'),),follow=True, callback='parse_item'),)

  def parse_item(self, response):
    schema = 'zhushou360://'
    item = QhItem()
    download_str = response.selector.css('.js-downLog').xpath('@href').extract()[0]
    item['file_urls'] = urlparse.parse_qs(download_str[download_str.find(schema) + len(schema):])['url']
    item['display_name'] = response.selector.css('#app-name span::text').extract()[0]
    item['rate_number'] = response.selector.css('.s-1::text').extract()[0]
    item['download_number'] = response.selector.css('.s-3::text').extract()[0][3:-1]
    return item
