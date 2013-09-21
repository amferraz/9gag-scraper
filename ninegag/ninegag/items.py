# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class NinegagItem(Item):
    entry_id = Field()
    url = Field()
    votes = Field()
    comments = Field()
    title = Field()
    img_url = Field()
