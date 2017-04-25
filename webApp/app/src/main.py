# -*- coding: utf-8 -*-
from textsearch import Indexer
from textsearch import Searcher
import functions 
import os
from search import search 
from rdflib import Graph
import sparqlQueries
from datetime import date, timedelta
import time


#results =  search("Sommer", "", "", "", False, False)
#(len(results))

g = Graph()
g.parse("index/ontology/nzz.nt", format="nt")
#print sparqlQueries.get_info("nzz_317", g)
print sparqlQueries.get_info("nzz_148", g)
print sparqlQueries.get_infos_author("Rainer Stadler", g)
print sparqlQueries.get_blog("Rainer Stadler", g)
print sparqlQueries.get_articles_on("2015-07-20", g)


#query_date = date.today() - timedelta(days=70) # 10, 70, 300, 3650
#print sparqlQueries.get_articles_on_range(query_date, 'Milosz Matuschek',  g)

""""
g = Graph()
g.parse("index/ontology/nzz.nt", format="nt")
start = time.time()
print sparqlQueries.get_info("nzz_1", g)
end = time.time()
print end - start



    
print "[Q] get author, date and title from an id (tdg_1194)"
print sparqlQueries.get_info("tga_248", g)
print

print "[Q] get all the articles for an author"
print sparqlQueries.get_articles("Rainer Stadler,", g)
print
print "[Q] get all the articles for a date"
print sparqlQueries.get_articles_on("2011-03-29", g)
print
print "[Q] all articles in the last <10> days/weeks/months/years "
query_date = date.today() - timedelta(days=70) # 10, 70, 300, 3650
print sparqlQueries.get_articles_on_range(query_date, g)
print 
print "[Q] check if article was written in the last <10> days/weeks/months/years "
query_date = date.today() - timedelta(days=70) # 10, 70, 300, 365
print sparqlQueries.was_it_written_on_range("tdg_866",query_date, g)

"""