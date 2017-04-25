# -*- coding: utf-8 -*-

import json, urllib2
import os
 
def twitter_shares(url): 
    response =  urllib2.urlopen("http://graph.facebook.com/?id="+ url) 
    html = response.read()
    data = json.loads(html)
    try:
        return data["shares"]
    except KeyError:
        return 0 

def encodeText(text):
    text = text.replace("ü", "ue")
    text = text.replace("ä", "ae")
    text = text.replace("ö", "oe")
    text = text.replace("ß", "ss")
    text = text.replace("Ü", "ue")
    text = text.replace("Ä", "ae")
    text = text.replace("Ö", "oe")
    
    textnew = ''.join([i if ord(i) < 128 else ' ' for i in text])
   
    return textnew



def getIdx(blog):
    
    direc = 'Scraping/indexing/index/texts' + blog + '/'
    ext = '.txt' # Select your file delimiter

    file_dict = {} # Create an empty dict

    # Select only files with the ext extension
    txt_files = [i for i in os.listdir(direc) if os.path.splitext(i)[1] == ext]
    return len(txt_files)


