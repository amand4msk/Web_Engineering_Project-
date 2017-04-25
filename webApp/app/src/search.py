# -*- coding: utf-8 -*-
from rdflib import Graph

from textsearch import Searcher
import functions 
import os
from item import Item
from datetime import date, timedelta

import sparqlQueries as sparql 

def getMult(time):
   
    print("time")
    print(time)
    time = int(time)
    if time == 1: return 1
    elif time == 2: return  7
    elif time == 3: return  30
    elif time == 4: return  365
    else: return 0

def search(query, title, stemmed, syn):

    print(query)
    if not query == None:
        q = unicode(query)
        searcher = Searcher() 
        allresults = searcher.search(q, title==True, stemmed==True, syn==True )   
        return allresults
    

def get_infos(nids,count, graphs):
   
    #g.parse("index/ontology/nzz.rdf")
    items = [] 
    for nid in nids:

        site = nid[0:nid.index("_")].replace("'", "")
        infos = sparql.get_info(nid, graphs[site])
        if len(infos) > 0:
            item = Item(infos[0][0].decode("UTF-8"), infos[0][1], infos[0][2].decode("UTF-8"), infos[0][4])
        else:
            item = Item("Not known", "" , "", "")
    
        items.append(item)
            
    return items
    
def get_infos_author(author, g):
    articles = sparql.get_infos_author(author, g)

        
    return articles

def get_texts(nids):
    
    texts = []
    dir = os.path.dirname(__file__)
    for nid in nids:
        nid = nid.replace("'", "")
        nid = nid.replace(".txt", "")
        blog = nid[0:nid.index('_')]
        text = open(dir +"/index/texts/" + blog + "/" + nid[0:len(nid)] +".txt" , 'r').read().decode('UTF-8')
        textShort = text[0:300]
        texts.append(textShort)
        
    return texts

def get_articles_for_author(author, graphs):
    
    articles = []
    for g in graphs:
        r = sparql.get_articles(author, graphs[g])
       
        if not r== None: articles = articles  + r

        
    return articles

def get_articles_on(date, graphs):
    articles = []
    for g in graphs:
        r = sparql.get_articles_on(date,  graphs[g])
        if not r == None: articles = articles + r
        
    return articles

def get_articles_on_range(timeSpan,time, graphs):
    articles = []
    mult = getMult(time)
    query_date = date.today() - timedelta(days=mult*timeSpan) 
    for g in graphs:
        r = sparql.get_articles_on_range_date(query_date, graphs[g])
        if not r == None: articles = articles + r
    
    return articles


def get_articles_on_range_author(author, timeSpan,time, graphs):
    articles = []
    mult = getMult(time)
    print(mult)
   
    query_date = date.today() - timedelta(days=mult*timeSpan) 
    print(query_date)
    for g in graphs:
        r = sparql.get_articles_on_range_date_author(query_date, author, graphs[g])
        if not r == None: articles = articles + r
    
    return articles

def get_blogname_form_author(author, g):
    return sparql.get_blogname_form_author(author, g)



            


