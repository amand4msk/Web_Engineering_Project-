# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from Scraping.items import BlogsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
import re 
from ConfigParser import SafeConfigParser
j = 0

class TgaSpider(CrawlSpider):
    name = 'tga'
        
    try:
        cfgPath ="settings/project.ini"
              
        parser = SafeConfigParser()
        parser.read(cfgPath)
        j = parser.get('tga', 'nextid')
    except IOError:
        j = 0
    
    start_urls = ['http://blog.tagesanzeiger.ch/']

    rules = [Rule(LinkExtractor(allow=[r'^http:\/\/blog\.tagesanzeiger\.ch\/((?!replytocom).)*$']), callback='parse_blogpost', follow=True)]
    
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
        global j
        pattern = r'^http:\/\/blog\.tagesanzeiger\.ch\/[^\/]+\/index\.php\/\d+\/[^\/]+\/$'
        prog = re.compile(pattern)
        result = prog.match(response.url)
        
        if result==None: 
            return
        author = ""
        date = ""
        title = ""
        blog_name = ""
        category = ""
        
        
        sel = Selector(response)
        item = BlogsItem()
        # Extract title
        item['url'] = response.url
        date = sel.xpath("//div[@class='article-date']/text()").extract()
        title = sel.xpath("//title/text()").extract()
        category = sel.xpath("//div[@class='article-meta']/div[@class='article-meta-cat']/a/text()").extract()
     
        text = sel.xpath("//div[@class='article-content']").extract()
        
        

        if len(date) > 0:
            value = date[0]
            try:

                author = value[4:value.index(',')]
                date= value[value.index(',')+2:]
            except ValueError:
                date = value
                author = ""
        else:
            
            date = sel.xpath("//footer[@class='publicationDate']/p/text()").extract()
            
            if len(date) > 0:
                value = date[0]
                try:
                    date= value[value.index('Publiziert am ')+len('Publiziert am  '):]
                except ValueError:
                    ""

        if len(text) < 1:
            text = sel.xpath("//div[@id='content']").extract() 
            if date == "" or len(date) == 0:
                s = sel.xpath("//div[@id='content']/small/text()").extract() 
                try:
                    value = s[0]
                    author = value[:value.index(' am')]
                    date = value[value.index('den')+4:]
                except IndexError:
                      ""
                except ValueError:
                      ""
   
        if len(text) < 1:
            text = sel.xpath("//div[@class='mainText']").extract() 

            
        item['article'] = 'tga_'+str(j)
        j +=1 
        if len(title) > 0:
            t = title[0]
            title = t[:t.index('|')]
            title = unicode(title)
            blog_name =unicode(t[t.index('|')+1:]).strip()
        if len(category) > 0: category = unicode(category[0])
                          
        if author != "": author = unicode(author)
      
        item['title'] = title
        item['category']= category
        item['author'] = author
        item['date'] = date
        item['twitter'] = "" 
        item['authorUrl']= ""
        item['blog_name'] = blog_name
        
                
        if len(text) > 1:
            text = self.getContent(text[0])
            f = open('Scraping/indexing/index/texts/tga/tga_' + str(j) + '.txt', 'w')
            f.write(text.encode('utf-8'))
            f.write("\n" + " " + "\n")

        return item

