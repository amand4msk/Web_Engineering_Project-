# -*- coding: utf-8 -*-

def encodeText(text):
    
    textUnicode = ""
    
    for word in text.split(" "):
        #word = replaceStuff(word)
        
        try:
            word = unicode(word)
        except UnicodeDecodeError:
            word = ""
        textUnicode += word + " "
    return textUnicode
    
def replaceStuff(text):

    text = text.replace("ü", "ue")
    text = text.replace("ä", "ae")
    text = text.replace("ö", "oe")
    text = text.replace("ß", "ss")
    text = text.replace("Ü", "ue")
    text = text.replace("Ä", "ae")
    text = text.replace("Ö", "oe")
    #text = text.encode('ascii',errors='ignore')
    return text




