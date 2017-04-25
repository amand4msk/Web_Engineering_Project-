# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, csv
import codecs
import os
import functions

class ScrapingPipeline(object):
    def process_item(self, item, spider):
        return item
    
    
class BlogsPipeline(object):

    def open_spider(self, spider):
        path =  os.path.dirname(__file__)
        file = path + '/indexing/jsonFiles/%s.json' % spider.name
        self.urls_seen = []
        try:
            text = open(file).read()
            data = json.loads(text)   
            for site in data:
                url = site['url']
                self.urls_seen.append(url)
        except ValueError:
            return 
            

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            f = open("duplicates.txt", "a")
            f.write(item['url'])
            f.close() 
            raise DropItem("Duplicate item found: %s" % item)
        return item
    
class JsonWithEncodingPipeline(object):

        
    def openJsonFile(self, path):
        try:
            file = open(path, 'r')
            text = file.read()
            file.close()
            print(text[len(text)-1:len(text)])
            if text[len(text)-1] == ']':
                file = open(path, 'w')
                file.write(text[:len(text)-1])
                file.write(",")
                file.close()
        except IOError:
            return
        except IndexError:
            return
            
    def initJsonFile(self, path):
        file = open(path, 'w')
        file.write("[")
        file.close()
    
    
    def open_spider(self, spider):
        path =  os.path.dirname(__file__)
        pathJson = path + '/indexing/jsonFiles/%s.json' % spider.name
        if not os.path.exists(pathJson):
            self.initJsonFile(pathJson)
        self.openJsonFile(pathJson)
        self.file = codecs.open(path + '/indexing/jsonFiles/%s.json' % spider.name, 'a', encoding='utf-8')
        

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        #self.file.write("]")
        self.file.close()
        
        