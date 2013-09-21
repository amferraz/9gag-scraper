# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from ninegag.items import NinegagItem
from scrapy.settings import Settings
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request


class NinegagSpider(BaseSpider):
    name = "9gag"
    allowed_domains = ["9gag.com"]
    start_urls = [
        "http://9gag.com/"
    ]


    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        last_gag_id = None
        for article in hxs.select('//article'):
            gag_id = article.select('@data-entry-id').extract()

            if gag_id:
                last_gag_id = gag_id[0]
                ninegag_item = NinegagItem()
                ninegag_item['entry_id'] = gag_id[0]
                ninegag_item['url'] = article.select('@data-entry-url').extract()[0]
                ninegag_item['votes'] = article.select('@data-entry-votes').extract()[0]
                ninegag_item['comments'] = article.select('@data-entry-comments').extract()[0]
                ninegag_item['title'] = article.select('.//h2/a/text()').extract()[0].strip()
                ninegag_item['img_url'] = article.select('.//a/@data-img').extract()[0]

                yield ninegag_item

        next_url = 'http://9gag.com/?id=%s&c=200' % last_gag_id
        yield Request(url=next_url, callback=self.parse)
