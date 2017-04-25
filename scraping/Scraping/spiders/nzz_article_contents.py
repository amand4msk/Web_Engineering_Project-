# -*- coding: iso-8859-1 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from Scraping.items import Blog
from Scraping.items import BlogsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
import os, time, json
import csv
import Scraping.functions 
from ConfigParser import SafeConfigParser
import nltk

class NzzArticleContentsSpider(CrawlSpider):
    name = "nzz"
    rules = [Rule(LinkExtractor(allow=[r'^http://www.nzz.ch\/meinung\/blogs\/.*[^\/]\/\?page=\d+']), callback='parse_blogpost', follow=True)]


    def __init__(self, configfile=None, category=None, *args, **kwargs):
        self.urs_seen = []
        self.path = ""
        self.dir =  os.path.dirname(__file__)
        super(NzzArticleContentsSpider, self).__init__(*args, **kwargs)

        self.start_urls = []
    
        try:
            cfgPath ="settings/project.ini"
              
            parser = SafeConfigParser()
            parser.read(cfgPath)
            self.j = int(parser.get('nzz', 'nextid'))
        except IOError:
            self.j = 0
    
        file = open(self.dir + '/urlsNzz.txt')
        lines = file.readlines()
        for line in lines:
            self.urs_seen.append(line[:-1])
    
        #print urls_seen
    
       
        reader = csv.reader(open("blogs.csv"))
        
        for row in reader:
            self.start_urls.append("http://www.nzz.ch/" +  row[0])
        del self.start_urls[-1]
      
        print self.urs_seen

    def getContent( self, content):
        try:
            idx = content.index("<p>")
            idx2 = content.rindex("</p>")   
                    
            text = content[idx:idx2]
            
            script = True
            
            while script:
                try:
                    idx = text.index("<script")
                    idx2 = text.index("</script>") + len("</script>")
                    text1 = text[:idx]
                    text2 = text[idx2:]
                    text = text1 + text2
                except ValueError:
                    script = False
    
            while True: 
                try:
                    idx1 = text.index("<")
                    idx2 = text.index(">")
                    text1 = text[:idx1]
                    text2 = text[idx2+1:]
                    text = text1 + text2
                except ValueError:      
                    return text.replace(',', ' ')
        except ValueError:
            return ""

        
           
    def parse_blogpost(self, response):
        sel = Selector(response)
        links = sel.xpath("//a[@class='title__name']/@href").extract()
        
        contents =  sel.xpath("//article[@class='content content--blog']").extract()
        authors = sel.xpath("//div[@class='brief__text']/a[contains(@href,'meinung')]/text()").extract()
        categories = sel.xpath("//div[@class='content__subcategories']/a/text()").extract()
        dates = sel.xpath("//span [@class='brief__time']/text()").extract()
        titles = sel.xpath("//a[@class='title__name']/text()").extract() 
        blog_name = sel.xpath("//title/text()").extract()
        authorUrls=sel.xpath("//div[@class='brief brief--author']/a[contains(@href, 'autor')]/@href").extract() 
        twitters = sel.xpath("//div[@class='brief__text']").extract()
        items = []
        
       
        outfile = open(  self.dir +  '/urlsNzz.txt', 'a')
        
        for i in range(0, len(links)):
            link = "http://www.nzz.ch" + links[i]
            
            if link in self.urs_seen:
                continue 
            
            content = contents[i]
            text = self.getContent(content)
            title = titles[i]
            
            item = BlogsItem()
            item['url'] = link
            item['author'] = authors[i][:-2]
            item['date'] = dates[i]
            item['category'] = categories[i]
            item['title'] = title
            item['article'] = 'nzz_'+str(self.j)
            item['blog_name'] = blog_name[0]
            item['authorUrl'] = "http://www.nzz.ch" + authorUrls[i]
            item['twitter'] = self.getTwitter(twitters[i])
                
            outfile.write(link + "\n")
            
            f = open('Scraping/indexing/index/texts/nzz/nzz_' + str(self.j) + '.txt', 'w')
            f.write(text.encode('utf-8'))
            f.write("\n" + " " + "\n")

            items.append(item)
            self.j += 1
            f.close()
            
        outfile.close()
        return items
     
   
   
  # span class="brief__authorname">von </span><a href="/meinung/blogs/uebermorgen/autor/bettinahoechli1/">Bettina Höchli, </a><span class="brief__time"> am 29. Oktober 2015, 10:33 Uhr</span>