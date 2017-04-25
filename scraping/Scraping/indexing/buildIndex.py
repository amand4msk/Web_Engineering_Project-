# -*- coding: utf-8 -*-
from textsearch import Indexer

import functions 
import os
import json
import codecs

from ontology import create_individuals, save_individuals_file
from ont_rdflib import create_ontology

import os

def index(path, textFiles, blog):
    indexer = Indexer()

    i = 0
    dir  = os.path.dirname(os.path.abspath(__file__)) + "/index/texts/" + blog 
    

    for file in os.listdir(dir):
        if file.endswith(".txt"):

            print(i)
            i += 1 
            path = dir + "/" + file
            print(file[:-4])
            if os.path.exists(path):     
               
                f = open(path, 'r')
                if(file.find(".txt") > -1):
                    try:
                        title = textFiles[file[:-4]]
                    except KeyError:
                        continue
                else:
                    title = file
                    
                text =f.read()
                title = functions.encodeText(title)
                text = functions.encodeText(text)
                indexer.writeText(text, title, file[:-4])
    
    indexer.commit()
    
    
def build(blogs, languages, pathTexts, pathJsonFiles, pathOnt):
    for i in range(0,len(blogs)):
        print(blogs[i])
        textFiles = create_ontology(pathOnt, blogs[i], pathJsonFiles + blogs[i] + ".json", languages[i])
        print(textFiles)
        index(pathTexts + blogs[i], textFiles, blogs[i])
    
    

    
    