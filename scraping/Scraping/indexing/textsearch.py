# -*- coding: utf-8 -*-

from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser, query
from whoosh.lang.morph_en import variations
import snowballstemmer
import os
import json
import urllib2


class Indexer(object):
    
        def __init__(self):
            path = os.path.dirname(os.path.abspath(__file__))
            print(path)
            self.IX = open_dir(path + "/index/index")
            self.Writer = self.IX.writer()
            
            """
            if german == True:
                self.Stemmer = snowballstemmer.stemmer('german')
            else:
                self.Stemmer = snowballstemmer.stemmer('french')
            """
                       
        def writeText(self, text, titleText, idNr):  
 
            titleStemmedList =  self.Stemmer.stemWords(titleText.split());
            textStemmedList =  self.Stemmer.stemWords(text.split()); 
            
            
            titleStemm = ""
            textStemmed = ""
            
            for word in titleStemmedList:
                titleStemm += word + " "
            for word in textStemmedList:
                textStemmed += word + " " 
            
            self.Writer.add_document(title=u"'"+titleText+"'",
                                     titleStemmed=u"'"+titleStemm+"'", 
                                     content=u"'"+text+"'",
                                     contentStemmed=u"'"+textStemmed+"'", 
                                     nid=u"'"+idNr+"'")

        def commit(self):
            self.Writer.commit() 
            
class Searcher(object):
    
        def getGermanSynonyms(self, word):
            url = 'https://www.openthesaurus.de/synonyme/search?q=' + word +'&format=application/json'
            print(url)
            response = urllib2.urlopen(url)
            html = response.read()
            ustr_to_load = unicode(html, 'latin-1')
           # print(ustr_to_load)
            data = json.loads(ustr_to_load)
            
            synonyms = []
            for s in data['synsets']:
                for term in s['terms']:
                    if term['term'] not in synonyms and len(term['term'].split(" ")) == 1:
                        synonyms.append(term['term'])
                        
            return synonyms
    
        def search(self, q, stemmed, syn):
            path = os.path.dirname(__file__)
            ix = open_dir(path + "/index")
            parser = MultifieldParser(["title", "content"], ix.schema)   
            searcher = ix.searcher()   
            cp = qparser.OperatorsPlugin(And="&", Or="\|", AndNot="!")
            parser.replace_plugin(cp) 
            
            if syn == True:
                
                for w in q.split(" "):
                    synonyms =self.getGermanSynonyms(w)
                    synQ = "(" + w 
                    for s in synonyms:
                        synQ += "\|" + s
                    synQ += ")"
                    qNew = q.replace(w, synQ)
                q = qNew
            
            searchQuery = parser.parse(q)
            allresults = searcher.search(searchQuery, limit=None)       
             
            if stemmed == True:
                results = self.searchGermanStemmed(q,ix)
                allresults.upgrade_and_extend(results)
                results = self.searchFrenchStemmed(q, ix)
                allresults.upgrade_and_extend(results)
            
            
            print(searchQuery)
                
           
           
           
            return  allresults
       
        def searchGermanStemmed(self, q, ix):            
            stemmer = snowballstemmer.stemmer('german')
                
            parser = MultifieldParser(["title", "titleStemmed", "contentStemmed" ,"content"], ix.schema)
            queryStemmedList = stemmer.stemWords(unicode(q).split())
            q = ""
            for w in queryStemmedList:
                    q += w + " "

                
            searcher = ix.searcher()   
            cp = qparser.OperatorsPlugin(And="&", Or="\|", AndNot="!")
            parser.replace_plugin(cp) 
            searchQuery = parser.parse(q)
            print(searchQuery)
            results= searcher.search(searchQuery, limit=None)            
             
            return  results 
        
        def searchFrenchStemmed(self, q, ix):            
            stemmer = snowballstemmer.stemmer('french')             
            
            parser = MultifieldParser(["title", "titleStemmed", "contentStemmed" ,"content"], ix.schema)
            queryStemmedList = stemmer.stemWords(unicode(q).split())
            q = ""
            for w in queryStemmedList:
                q += w + " "

                
            searcher = ix.searcher()   
            cp = qparser.OperatorsPlugin(And="&", Or="\|", AndNot="!")
            parser.replace_plugin(cp) 
            searchQuery = parser.parse(q)
            print(searchQuery)
            results= searcher.search(searchQuery, limit=None)            
          
            return  results 
        
        
        
            
        def searchTest(self):
            result =  self.Searcher.search(Term("content", u"oberflaechen"))
            return result
            
        
            
             
    
