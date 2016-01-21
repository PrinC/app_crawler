import scrapy
import urlparse
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from app_crawler.items import MyappItem

class MyappSpider(CrawlSpider):
  name = "myapp"
  start_urls = ["http://android.myapp.com/myapp/category.htm?orgame=1"]
  rules = (Rule(LinkExtractor(allow=('detail\.htm'),),follow=True, callback='parse_item'),)

  def parse_item(self, response):
    item = MyappItem()
    item['parse_url'] = response.url;
    item['file_urls'] = response.selector.css('.det-down-btn').xpath('@data-apkurl').extract()
    if urlparse.urlparse(item['file_urls'][0]).netloc != 'dd.myapp.com':
      return
    item['display_name'] = response.selector.css('.det-name-int::text').extract()[0]
    item['package_name'] = response.selector.css('.det-ins-btn').xpath('@apk').extract()[0]
    item['rate_number'] = str(float(response.selector.css('.com-blue-star-num::text').extract()[0][:-1]) * 2)
    item['download_number'] = response.selector.css('.det-ins-num::text').extract()[0][:-2]
    item['update_time'] = response.selector.css('#J_ApkPublishTime').xpath('@data-apkpublishtime').extract()[0]
    return item
