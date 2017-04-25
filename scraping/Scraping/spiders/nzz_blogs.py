# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from Scraping.items import Blog
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

import re
import os, time, json

class NzzBlogsSpider(scrapy.Spider):
    name = "nzz_blogs"
    allowed_domains = ["http://www.nzz.ch/meinung/blogs"]
    start_urls = ['http://nzz.ch/meinung/blogs']

    def parse(self, response):
        
        sel = Selector(response)

        titles =  sel.xpath("//a[@class='container__head-link']/text()").extract()
        links =  sel.xpath("//a[@class='container__head-link']/@href").extract()
        items = []
        for i in range(0, len(titles)):
            item = Blog()
            print titles[i].encode('utf-8')
            item["name"] = unicode(titles[i])
            item["url"] = links[i]
            items.append(item)
        return items

