from rdflib import Graph

import pprint



 

def parse_results(qres):
  results = []
  for i, res in enumerate(qres):
    cur = []
    for lit in res:
      cur.append(str(lit.encode("utf-8")))
    results.append(cur)
  return results

def get_info(idx, g):
  qres = g.query(
    """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?hasAuthor ?hasDate ?hasTitle ?hasID ?hasUrl 
      WHERE {  
          ?a BlogsOntology:hasID ?hasID . FILTER (?hasID="%s"^^xsd:string) . 
          ?a BlogsOntology:hasDate ?hasDate .
          ?a BlogsOntology:hasTitle ?hasTitle .
          ?a BlogsOntology:hasAuthor ?hasAuthor .
          ?a BlogsOntology:hasUrl ?hasUrl .
       }
       LIMIT 1""" % idx)
  
  return parse_results(qres)

def get_articles(author, g):
    q=  """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?hasAuthor ?hasDate ?hasTitle ?hasID ?hasUrl 
      WHERE {  
          ?a BlogsOntology:hasAuthor ?hasAuthor . FILTER (?hasAuthor="%s"^^xsd:string) . 
          ?a BlogsOntology:hasDate ?hasDate .
          ?a BlogsOntology:hasTitle ?hasTitle .
          ?a BlogsOntology:hasID ?hasID .
          ?a BlogsOntology:hasUrl ?hasUrl .
       }""" % author
    qres = g.query(q)
   
  
    return parse_results(qres)

def get_infos_author(author,g):
    
    q=  """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?hasName ?hasTwitterAccount ?hasAuthorUrl
      WHERE {  
          ?a BlogsOntology:hasName ?hasName . FILTER (?hasName="%s"^^xsd:string) . 
          ?a BlogsOntology:hasTwitterAccount ?hasTwitterAccount .
          ?a BlogsOntology:hasAuthorUrl ?hasAuthorUrl .          
       }""" % author
    qres = g.query(q)
    return parse_results(qres)

def get_blog(author,g):
        
    q=  """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?hasBlogTitle ?hasAuthors 
      WHERE {  
          ?a BlogsOntology:hasBlogTitle ?hasBlogTitle . FILTER (?hasBlogTitle="%s"^^xsd:string) . 
          ?a BlogsOntology:hasAuthors ?hasAuthors .

       }""" % "Experiment Erde - NZZ Blogs"
    qres = g.query(q)
    return parse_results(qres)
    

def get_articles_on(date, g):
  qres = g.query(

    """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?title ?hasDate ?hasID ?hasUrl ?hasAuthor
      WHERE {
          ?a BlogsOntology:hasDate ?hasDate . FILTER(str(?hasDate) = '%s') .
          ?a BlogsOntology:hasTitle ?title .
          ?a BlogsOntology:hasID ?hasID . 
          ?a BlogsOntology:hasUrl ?hasUrl .
          ?a BlogsOntology:hasAuthor ?hasAuthor .
       }""" % date)

  return parse_results(qres)

def get_articles_on_range_date(date, g):
  qres = g.query(

    """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?title ?hasDate ?hasID ?hasUrl ?hasAuthor
      WHERE {
          ?a BlogsOntology:hasDate ?hasDate . FILTER(str(?hasDate) >= '%s') .
          ?a BlogsOntology:hasTitle ?title .
          ?a BlogsOntology:hasID ?hasID . 
          ?a BlogsOntology:hasUrl ?hasUrl .
          ?a BlogsOntology:hasAuthor ?hasAuthor .
       }""" % date)

  return parse_results(qres)

def get_articles_on_range_date_author(date, author, g):
  qres = g.query(

    """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?title ?hasDate ?hasID ?hasUrl ?hasAuthor
      WHERE {
          ?a BlogsOntology:hasDate ?hasDate . FILTER(str(?hasDate) >= '%s') .
          ?a BlogsOntology:hasTitle ?title .
          ?a BlogsOntology:hasID ?hasID . 
          ?a BlogsOntology:hasUrl ?hasUrl .
          ?a BlogsOntology:hasAuthor ?hasAuthor . FILTER(str(?hasAuthor) = '%s') .
       }""" % (date, author))

  return parse_results(qres)


def was_it_written_on_range(article, date, g):
  qres = g.query(

    """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?title ?hasDate
      WHERE {
          ?a BlogsOntology:hasID ?hasID . FILTER( ?hasID = '%s') .
          ?a BlogsOntology:hasTitle ?title .
          ?a BlogsOntology:hasDate ?hasDate . FILTER(str(?hasDate) >= '%s') .
       }""" % (article,date))

  return parse_results(qres)



def get_blogname_form_author(author, g):
  qres = g.query(
    """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?hasBlogTitle
      WHERE {   
          ?a BlogsOntology:hasName ?hasName . FILTER (?hasName="%s"^^xsd:string) . 
          ?element BlogsOntology:hasAuthors ?a . 
          ?element BlogsOntology:hasBlogTitle ?hasBlogTitle . 

       }""" % author)
  return parse_results(qres)


