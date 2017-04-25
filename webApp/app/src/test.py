import sparql

def get_info(idx):
  qres = """ PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX BlogsOntology: <http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#>
    SELECT ?hasName ?hasDate ?hasTitle ?hasID
      WHERE {  
          ?a BlogsOntology:hasID ?hasID . FILTER (?hasID="%s"^^xsd:string) . 
          ?a BlogsOntology:hasDate ?hasDate .
          ?a BlogsOntology:hasTitle ?hasTitle .
          ?b BlogsOntology:hasArticles ?a .
          ?b BlogsOntology:hasName ?hasName .
       }""" % idx
  return qres


q = get_infos_author("nzz_100")
result = sparql.query('index/ontology/nzz.rdf', q)

result.variables