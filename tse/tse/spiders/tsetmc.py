# -*- coding: utf-8 -*-
import datetime

import scrapy
from tse.items import StockDayDetail


class TsetmcSpider(scrapy.spiders.CrawlSpider):
    name = 'tsetmc'
    allowed_domains = ['cdn.tsetmc.com', 'tsetmc.com']
    start_urls = []
    url_format = "http://cdn.tsetmc.com/Loader.aspx?ParTree={partree}&i={code}&d={date}"

    def __init__(self, partree=None, code=None, start_date=None, end_date=None, *args, **kwargs):
        super(TsetmcSpider, self).__init__(*args, **kwargs)
        if code is None or partree is None:
            self.log(f"You need to specify what you want to crawl")
            raise ValueError(f"{partree} is not a valid input.")
        if end_date is None:
            end_date = datetime.datetime.today()
        else:
            try:
                end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
            except ValueError as e:
                self.log(e)

        if start_date is None:
            start_date = datetime.datetime.today() - datetime.timedelta(days=7)
        else:
            try:
                start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
            except ValueError as e:
                self.log(e)
        self.start_date = start_date
        self.end_date = end_date
        self.partree = partree
        self.code = code

    def start_requests(self):
        d = self.start_date
        while d <= self.end_date:
            yield scrapy.Request(self.url_format.format(
                partree=self.partree,
                code=self.code,
                date=d.strftime("%Y%m%d")))
            d += datetime.timedelta(days=1)

    def parse(self, response):
        item = StockDayDetail()
        item['raw_data'] = response.xpath("//script//text()[contains(.,'var BestLimitData')]").getall()
        item['header'] = response.css('div.header').css('.bigheader').xpath(".//span//text()").getall()
        self.log('page crawled.')
        yield item
