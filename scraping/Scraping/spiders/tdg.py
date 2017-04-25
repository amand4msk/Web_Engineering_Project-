import nltk
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from Scraping.items import Blog
from Scraping.items import BlogsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from pprint import pprint
from bs4 import BeautifulSoup
import urllib2
import httplib
from urlparse import urlparse
from ConfigParser import SafeConfigParser



class TDGSpider(CrawlSpider):

    name = 'tdg'
   
    rules = [Rule(LinkExtractor(allow=[r'blog\.tdg\.ch\/archive\/\d+\/\d+\/\d+\/.+html$']), callback='parse_blogpost', follow=True)]
    
    def __init__(self, configfile=None, category=None, *args, **kwargs):
        super(TDGSpider, self).__init__(*args, **kwargs)
        
        self.authors = dict() 
        self.aboutUrls = dict() 
        
        try:
            cfgPath ="settings/project.ini"
                  
            parser = SafeConfigParser()
            parser.read(cfgPath)
            self.j = int(parser.get('tdg', 'nextid'))
        except IOError:
            self.j = 0
            
        self.start_urls = ['http://blog.tdg.ch/explore/blogs']  
    
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
                    return text  #.replace(',', ' ')
        except ValueError:
            return ""
    
    def parse_blogpost(self, response):
        sel = Selector(response)
        item = BlogsItem()

        # Extract title, date, url, article, author and the name of the blog which the article belongs to.
        blog = sel.xpath("//title/text()").extract()
        item['blog_name'] = ""
        if len(blog) > 0:
            if blog[0].find(':') > -1:
                blog_name = blog[0].split(':')
                item['blog_name'] = blog_name[-1]

        title = sel.xpath("////meta[@property='og:title']/@content").extract()
        item['title'] = title[0]
        item['date'] = sel.xpath("//h2[@class='date']/span/text()").extract()
        item['date'] = item['date'][0]
        text = sel.xpath("//*[@class='posttext-decorator2']").extract()
        #item['article'] = nltk.clean_html(' '.join(text))
       
        #text = nltk.clean_html(' '.join(text))
        #print(text)
        item['article'] = 'tdg_'+str(self.j)
        item['url'] = response.url
        
        f = open('Scraping/indexing/index/texts/tdg/tdg_' + str(self.j) + '.txt', 'w')
        f.write(self.getContent(text[0].encode("utf-8")))
        f.write("\n" + " " + "\n")

        self.j +=1 
        
        #import pdb;pdb.set_trace() --Debugging command!
        # Extracting the author from the url/about.html 
        # Doing individual crawling with beautifulSoup in this page and extract the h3 tag to return the author


        url = item['url'].split('/')[2] + '/about.html'
        
        if url not in self.authors:
            about = item['url'].split('/')[2] + '/about.html'
            about_http = 'http://' + about
            #if self.checkUrl(about_http):
            try:    
                html_about = urllib2.urlopen(about_http).read()
                soup = BeautifulSoup(html_about) # making soap
                item['author'] = soup.select("h3")[0]
                item['author'] = item['author'].get_text()  
                item['authorUrl'] = about_http
                
                self.authors[url] = item['author']
                self.aboutUrls[url] = item['authorUrl'] 
            except:
                print "FAILED PROCESSING ABOUT PAGE"
                pass  
        else:
            print("have about already")
            item['author'] = self.authors[url]
            item['authorUrl'] = self.aboutUrls[url]
            
        
          
        return item
 

    def checkUrl(self, url):
        p = urlparse(url)
        conn = httplib.HTTPConnection(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        return resp.status < 400
  
