import scrapy
import urlparse
import re
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from app_crawler.items import QhItem

class QhSpider(CrawlSpider):
  name = "qh"
  allowed_domains = ["360.cn"]
  start_urls = ["http://zhushou.360.cn/detail/index/soft_id/433"]
  rules = (Rule(LinkExtractor(allow=('detail\/index\/soft_id'),),follow=True, callback='parse_item'),)

  def parse_item(self, response):
    schema = 'zhushou360://'
    item = QhItem()
    download_str = response.selector.css('.js-downLog').xpath('@href').extract()[0]
    item['parse_url'] = response.url;
    item['file_urls'] = urlparse.parse_qs(download_str[download_str.find(schema) + len(schema):])['url']
    item['display_name'] = response.selector.css('#app-name span::text').extract()[0]
    item['rate_number'] = response.selector.css('.s-1::text').extract()[0]
    item['download_number'] = response.selector.css('.s-3::text').extract()[0][3:-1]
    item['package_name'] = re.findall(r'\'pname\'\:\s"(.*?)"', response.body)
    return item
