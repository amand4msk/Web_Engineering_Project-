# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class BlogsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    title = Field()
    author = Field()
    date = Field() 
    twitter = Field()
    category = Field() 
    article = Field() 
    blog_name = Field()
    twitter = Field() 
    authorUrl = Field()
    

class Blog(Item):
    name = Field()
    url = Field() 


class ArticleText(Item):
    url= Field()
    text = Field() 
