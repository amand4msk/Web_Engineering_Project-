#!flask/bin/python
from rdflib import Graph, BNode, Literal, URIRef

from app import app


app.run(debug=True)
