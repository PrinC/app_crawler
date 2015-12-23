import scrapy
import urlparse
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from app_crawler.items import BaiduItem

class BaiduSpider(CrawlSpider):
  name = "baidu"
  allowed_domains = ["baidu.com"]
  start_urls = ["http://shouji.baidu.com/software/"]
  rules = (Rule(LinkExtractor(allow=('\/soft\/item'),),follow=True, callback='parse_item'),)

  def parse_item(self, response):
    item = BaiduItem()
    item['file_urls'] = response.selector.css('.inst-btn-big').xpath('@data_url').extract()
    item['package_name'] = response.selector.css('.inst-btn-big').xpath('@data_package').extract()[0]
    item['display_name'] = response.selector.css('.app-name span::text').extract()[0]
    item['rate_number'] = str(int(response.selector.css('.star-percent').xpath('@style').extract()[0][6:-1])/10.0)
    item['download_number'] = response.selector.css('.detail .download-num::text').extract()[0][5:]
    return item
