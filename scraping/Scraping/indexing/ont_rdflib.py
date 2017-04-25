# -*- coding: utf-8 -*-

import json
import codecs
from rdflib import URIRef, BNode, Literal, Namespace, Graph
from rdflib.namespace import RDF, XSD, RDFS
import rdflib
import os 

i=0

def load_data(fname):
	with open(fname) as data_file:    
		data = json.load(data_file)
	return data

def escape(text):
	text = text.replace("&"," and ")
	text = text.replace("<"," less than ")
	text = text.replace(">"," greater than ")
	return text


def canonicalize_french(date):
	# Most of them were: e.g. mardi, 2 mars 2010 so 
	# I converted to 2/03/2010 (AT first and then I put it in the date_convert function)
	if date.find(",") > -1:
		date = date.lower().split(",")[1].strip()
	else:
		date = date.lower().strip()
	date = date.encode('utf-8')
	fr_months = ['janvier', 'f\xc3\xa9vrier', 'mars', 'avril', 
				 'mai', 'juin', 'juillet', 'ao\xc3\xbbt', 'septembre', 
				 'octobre', 'novembre', 'd\xc3\xa9cembre']
	for x, month in enumerate(fr_months):
		j = x+1
		if j < 9:
			num = "0%d" % j
		else:
			num = "%d" % j 
		date = date.replace(month, num)
	date = "/".join(date.split(" "))
	return date

def canonicalize_german(date):
	# Most of them were: e.g. mardi, 2 mars 2010 so 
	# I converted to 2/03/2010 (AT first and then I put it in the date_convert function)
	
	if date.find('am') > -1:
		date = date[date.index('am') + len('am '):]
	
	if date.find(",") > -1:
		date = date.lower().split(",")[0].strip()
	else:
		date = date.lower().strip()
		
	date = date.encode('utf-8')
	de_months = ['januar', 'februar', 'märz', 'april', 
				 'mai', 'juni', 'juli', 'august', 'september', 
				 'oktober', 'november', 'dezember']
	for x, month in enumerate(de_months):
		j = x +1 
		if j < 9:
			num = "0%d" % j
		else:
			num = "%d" % j 
		date = date.replace(month, num)
	date = "/".join(date.split(" "))
	date = date.replace(".", "")
	return date


def date_convert(date):
	# convert 2/03/2010 to 2010/03/2
	if date != "":
		toks = date.split("/")
		if len(toks) == 3:
			return "%s-%s-%s" % (toks[2], toks[1], toks[0])
		else:
			return ""
	else:
		return ""
def create_ontology(pathOnt, blog, file, language):
	n = Namespace("http://www.semanticweb.org/amanda/ontologies/2015/10/BlogsOntology#")
	from rdflib.plugins import sleepycat
	g = Graph()
	path =  os.path.dirname(__file__)

	g.parse(path + "/BlogsOntology2.xml") # our ontology schema
	
	#sites = [URIRef('http://example.org/tdg'), URIRef('http://example.org/nzz')] # here put the name of your site
	#site_literals = ['tdg', 'nzz'] #here in the second element put the name of your site instead of nzz :)

	#site_data = ['data-fixed-all.txt', 'data_nzz.txt'] 
	# in the second element instead data_nzz.txt you put your file
	#and your file should has the format [{...},{....},{....},...]

	site = URIRef('http://example.org/' + blog)
	site_literal = blog
	site_data = file
	
	g.add( (site, n['hasSiteTitle'], Literal(site_literal,  datatype=XSD.string) ) )
	print(file)
	data = load_data(site_data)
	blog_set = {}
	author_set = {}
	individuals = []
	c = 0
	bid = 0
	aid = 0
	textfiles = dict()

	for idx, line in enumerate(data):
		# Here check all the e.g. line['blog_name'] if we have the same name 
		# Otherwise change the 'blog_name' with yours from your file

		
		print "(%d/%d)" % (idx, len(data))
		if isinstance(line["title"], list):#if it is array convert to string
			line["title"] = " ".join(line["title"]) 
			# some of my titles printed in ontology as [u'blabla'] and I converted as a atrng
		if isinstance(line["date"], list):#if it is array convert to string
			line["date"] = " ".join(line["date"])
			# some of my dates printed in the ontology as [u'blabla'] and I converted as a atrng 
			#so if you don;t have this problem just put in a comment
			
			
		#here just to inform you the sparql accepts the format ONLY --> 2009-09-10 
		# so i convert all the dates that have the formats like: 16/11/1990, 02 mars 2010 etc to the correct way
		if line["date"].find('/') == -1:
			if language == 0: line["date"] = canonicalize_german(line["date"])	
			if language == 1:	line["date"] = canonicalize_french(line["date"])
			c+=1

		print line["date"]
		line["date"] = date_convert(line["date"])

		
		textfiles[line["article"] ] =   line["title"] 
		# here just to inform you in some titles and blog names there were the symbols &,>,< 
		# and i had an error because these symbols are special characters for xml and I just replaced them
		line["blog_name"] = escape(line["blog_name"]).strip()
		line["title"] = escape(line["title"]).strip()

		if 'author' in line:# Maria, this line (if 'author' in line:) put it in comment :)
			line["author"] = line["author"].strip()
			bname = line['blog_name']
			aname = line['author']

			try:
				twitter=line["twitter"]
			except KeyError:
				twitter = "-"

			if aname not in author_set:
				author_set[aname] = URIRef('http://example.org/author_%d' % aid)
				#about = line['url'].split('/')[2] + '/about.html'
				g.add( (author_set[aname], n['hasName'], Literal(aname,  datatype=XSD.string) ) )
				g.add( (author_set[aname], n['hasTwitterAccount'], Literal(twitter,  datatype=XSD.string) ) )
				#here put your user twitter account instead of '-'
				g.add( (author_set[aname], n['hasAuthorUrl'], Literal(line['authorUrl'],  datatype=XSD.string) ) )
				#and in the about variable (for the author url) put your url and also put in comment the line 102
				aid +=1 

			if bname not in blog_set:
				blog_set[bname] = URIRef('http://example.org/blog_%d' % bid)
				g.add( (site, n['hasBlogs'], blog_set[bname] ) )
				g.add( (blog_set[bname], n['hasBlogTitle'], Literal(bname,  datatype=XSD.string) ) )
				g.add( (blog_set[bname], n['hasAuthors'], author_set[aname] ) )
				bid +=1

		article = URIRef('http://example.org/article_%d' % idx)
		#g.add( (author_set[aname], n['hasArticles'], article ) )
		g.add( (article, n['hasTitle'], Literal(unicode(line["title"]),  datatype=XSD.string) ) )
		g.add( (article, n['hasUrl'], Literal(line["url"],  datatype=XSD.string) ) )
		g.add( (article, n['hasDate'], Literal(line["date"],  datatype=XSD.date) ) )
		g.add( (article, n['hasID'], Literal(line["article"],  datatype=XSD.string) ) )
		g.add( (article, n['hasAuthor'], Literal(line["author"],  datatype=XSD.string)))
				#blogs.append(bname)
				#authors.append(aname)
				#urls.append(line["url"])

	print g.serialize(format='pretty-xml')
	nameOnt = pathOnt  +  blog + ".nt"
	#g.serialize(nameOnt)
	g.serialize(nameOnt, format='nt')
 	return textfiles

def main():
	create_ontology()
	
if __name__ == '__main__':
	main()	