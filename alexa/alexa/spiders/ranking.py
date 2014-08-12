from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from alexa.items import RankingItem

class RankingSpider(CrawlSpider):
    
    name = 'ranking'
    start_urls = ['http://www.alexa.com/topsites/countries;0/US']
    rules = [Rule(LinkExtractor(allow=["/topsites/countries;\d+/US"]), 'parse_ranking')]
    
    def _decription(self, site):
        description = site.xpath("div/div[@class='description']/text()").extract()
        remainder = site.xpath(
            "div/div[@class='description']/span[@class='remainder']/text()"
        ).extract()
        return description + remainder
        # return [''.join(description + remainder)]

    def parse_ranking(self, response):
        items = []
        for site in response.xpath("//li[@class='site-listing']"):
            item = RankingItem()
            item['id'] = site.xpath('div/p/a/text()').extract()
            item['rank']  = site.xpath("div[@class='count']/text()").extract()
            item['descripton'] = self._decription(site)
            items.append(item)
        return items
