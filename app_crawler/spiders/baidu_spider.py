import scrapy
import urlparse
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from app_crawler.items import BaiduItem

class BaiduSpider(CrawlSpider):
  name = "baidu"
  start_urls = ["http://shouji.baidu.com/software/"]

  rules = (Rule(LinkExtractor()))
  rules = (Rule(LinkExtractor(allow=('\/software\/item'),),follow=True, callback='parse_item'),)

  def parse_item(self, response):
    item = BaiduItem()
    item['parse_url'] = response.url;
    item['file_urls'] = response.selector.css('.area-download .apk').xpath('@href').extract()
    if urlparse.urlparse(item['file_urls'][0]).netloc != 'p.gdown.baidu.com':
      raise DropItem('Not baidu official app');
    item['display_name'] = response.selector.css('.app-name span::text').extract()[0]
    item['rate_number'] = str(int(response.selector.css('.star-percent').xpath('@style').extract()[0][6:-1])/10.0)
    item['download_number'] = response.selector.css('.detail .download-num::text').extract()[0][5:]
    return item
