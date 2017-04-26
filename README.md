## Seminar Project


In this project we created a web crawler using Scrapy and crawled three French-German blogs (“Tagesanzeiger”, “Neue Züricher Zeitung” and “Tribune de Genève”.). First, we extracted all the relevant data of these blogs. Using these data, we built our blog ontology using Protégé for creating the RDF schema and RDFLib for instances.

Moreover, for the metadata search we used the ontology and for the text search (terms in title and content of the article) we built an index. We also created a synonym expansion only for German language. Finally, a user has the ability to search in the data by using our web application in Flask framework.


## Install (Ubuntu)

```
pip install -r requirements.txt
```

## Crawling 

Crawling is not automated at the moment. Thus, to start a new crawling you have to start the process from the command line:


Change directory to the scraping application:
```
cd pathToProject/Project/scraping 
```


Crawl for the NZZ blogs:
```
scrapy crawl nzz_blogs -o blogs.csv -t csv
```


Crawl the NZZ blogs:
```
scrapy crawl nzz
```


Crawl the Tagesaneziger:
```
scrapy crawl tga
```


Crawl Tribune de Geneve:
```
scrapy crawl tdg
```

## Building the index


After the crawling, the index and ontology have to be updated. If the index was never before initialized the script `create_schema.py` under `Project/Scraping/scraping/indexing` has to be called. For every other one just has to run the script `main.py` in the root folder. This scripts updates the index and ontology and copies all the text files and index files to the Web application. 


## Running webserver 

```
cd pathToProject/Project/WebApp 
./run.py

Starts server: localhost:5000
```

## report

This folder contains a detailed description of the project.
