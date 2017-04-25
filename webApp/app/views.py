# -*- coding: utf-8 -*-

from flask import render_template
from app import app


import app.src.search as search

from forms import  PostForm
from flask import request
import flask.ext.whooshalchemy
#import sparql
from flask import Flask, current_app
from rdflib import Graph


resultsNid = []
g_nzz = Graph()
g_nzz.parse("app/src/index/ontology/nzz.nt", format ="nt") 

g_tdg = Graph()
g_tdg.parse("app/src/index/ontology/tdg.nt", format ="nt") 

g_tga = Graph()
g_tga.parse("app/src/index/ontology/tga.nt", format ="nt") 

graphs = {'nzz' : g_nzz, 'tdg' : g_tdg, 'tga' : g_tga }

print("parsing")

def getItems():
    posts = []
 
    if len(resultsNid) > 4:
        i = 5
    else:
        i = len(resultsNid)
        
    items = search.get_infos(resultsNid[0:i], 5, graphs)   
    texts = search.get_texts(resultsNid[0:i])
    
    print(len(items))
    
    print(resultsNid) 
    for i in range(0,len(items)):
        post = {    'url':  items[i].Url,
                    'body': texts[i],
                    'author': items[i].Author,
                     'date': items[i].Date,
                    'title': items[i].Title,
                    'site': resultsNid[i][:resultsNid[i].index('_')]
                    }
        posts.append(post)
    
    del resultsNid[0:i]  
    print(len(posts))
    return posts


def getNidsForAuthor(author, graphs):
    articlesForAuthor = search.get_articles_for_author(author, graphs)
               
    resultsAuthor = []
    for article in articlesForAuthor:    
        resultsAuthor.append(unicode(article[3].replace("\"", "")))
    return resultsAuthor

def getNidsForDateRange(range, time, graphs):
    articlesForDate = search.get_articles_on_range(range, time, graphs)
    resultsDate = []
    for article in articlesForDate:
        resultsDate.append(unicode(article[2].replace("\"", "")))   
            
    return resultsDate           

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])      
def index():
    form = PostForm()
    
    #current_app._get_current_object.get_db

    global graphs
    global resultsNid
    
    text = ""
    stemmed = ""
    syn = ""
    title = ""
    author =""
    number = ""
    time = ""
   
    posts = []
    number = 0
        #if form.validate_on_submit():
    
    text = form.post.data
    stemmed = form.stemmed.data
    syn = form.syn.data
    title = form.title.data
    author = form.author.data
    numberTime = form.number.data
    time = form.time.data
    
   

    print(request.data)
    if 'search' in request.form:
        """
        print("text: " + text)
        print("stemmed: " + str(stemmed))
        print("syn: " + str(syn))
        print("title: " + str(title))
        print("author: " + author)
        print("number: " + str(numberTime))
        print("time: " + time)
        """
        
        resultsNid = []
        
        if not text == "":
        
            results = search.search(text, title, stemmed, syn)
            print(len(results))
            for result in results:
                resultsNid.append(result["nid"].replace("'", "").replace("\"", ""))   
            
            if not author == "":
                resultsAuthor = getNidsForAuthor(author, graphs)
                resultsNid = list(set(resultsNid) & set(resultsAuthor))
                
                if not numberTime == None:
                    resultsDate = getNidsForDateRange(numberTime, time, graphs)
                    resultsNid = list(set(resultsNid) & set(resultsDate))
                    
            elif not numberTime == None:
                resultsDate = getNidsForDateRange(numberTime, time, graphs)
                resultsNid = list(set(resultsNid) & set(resultsDate))   
            
            posts = getItems()
            print(posts)    
            
        elif not author == "":     
            if not numberTime == None:
                resultsDate = search.get_articles_on_range_author(author, numberTime, time, graphs)
                nids = []
                for article in resultsDate:
                    nids.append(str(article[2]) + ".txt")
                texts = search.get_texts(nids)
                posts = [] 
                for i in range(0, len(nids)):
                        post = {    'url':  resultsDate[i][3],
                                    'body': texts[i],
                                    'date': resultsDate[i][1],
                                    'title': resultsDate[i][0].decode("UTF-8"),
                                    'author': resultsDate[i][4],
                                    'site': nids[i].replace(".txt", "")
                                    }
                        posts.append(post)
            else:
                articles = search.get_articles_for_author(author, graphs)
                print(articles)
                nids = []
                for article in articles:
                    nids.append(str(article[3]) + ".txt")
                texts = search.get_texts(nids)
    
                posts = [] 
                for i in range(0, len(nids)):
                    post = {    'url':  articles[i][4],
                                'body': texts[i],
                                'date': articles[i][1],
                                'title': articles[i][2].decode("UTF-8"),
                                'site': nids[i].replace(".txt", "")
                    }
                    posts.append(post)
            
            
        
        if len(resultsNid) > 4:
             number = 5
        else:
            number = len(resultsNid)
            
        
    if 'next' in request.form:
        posts = getItems()
        
        if len(resultsNid) > 4:
            number = 5
        else:
            number = len(resultsNid)

    return render_template("index.html",
                                    title='Home',
                                    posts=posts,
                                    form=form,
                                    number=number)

#TODO : FOR ALL GRAPHS 
@app.route('/author')
def author():
    global graphs
    author = request.args.get('author')
    site = request.args.get('site')
    print(site)
    print(author)
    g = graphs[site]
    articles = search.get_articles_for_author(author, graphs)
    
    nids = []
    for article in articles:
        nids.append(str(article[3]))
    
    texts = search.get_texts(nids)
    
    posts = [] 
    for i in range(0, len(nids)):
        post = {    'url':  articles[i][4],
                    'body': texts[i],
                     'date': articles[i][1],
                    'title': articles[i][2].decode("UTF-8")
                    }
        posts.append(post)
        
    item = search.get_infos_author(author, g)
    blog = search.get_blogname_form_author(author, g)
    if len(blog) > 0:
        blogVal = blog[0][0]
    else:
        blogVal = ""
        
    if len(item) > 0:
        infos = {'articles' : len(nids),
                 'url' : item[0][2],
                'twitter': item[0][1],
                 'blog': blogVal.decode("UTF-8")}
    else:
        infos = {'articles' : len(nids),
                 'url' : "",
                'twitter': "",
                'blog': blogVal.decode("UTF-8")}
    
    return render_template("author.html",
                           title='Home',
                           author=author,
                           posts=posts,
                           infos=infos,
                           )

@app.route('/date')
def date():
    
    date = request.args.get('date')
    print(date)
    global graphs

    articles = search.get_articles_on(date, graphs)
    
    nids = []
    for article in articles:
        nids.append(str(article[2]) + ".txt")
    
    texts = search.get_texts(nids)
    
    posts = [] 
    for i in range(0, len(nids)):
        print(articles[i][3])
        post = {    'url':  articles[i][3],
                    'body': texts[i],
                    'title': articles[i][0].decode("UTF-8"),
                    'author': articles[i][4].decode("UTF-8")
                    }
        posts.append(post)
        
    
    return render_template("date.html",
                           title='Home',
                           posts=posts,
                           date=date,
                           number=len(articles)
                           
                           )


@app.route('/info')
def info():
     return render_template("info.html",
                           title='Info',
                           )