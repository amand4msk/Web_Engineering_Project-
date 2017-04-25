from whoosh.fields import Schema, STORED, TEXT, ID
import os.path
from whoosh.index import create_in
from whoosh.analysis import CharsetFilter, StemmingAnalyzer
from whoosh import fields
from whoosh.support.charset import accent_map



# For example, to add an accent-folding filter to a stemming analyzer:
my_analyzer = StemmingAnalyzer() | CharsetFilter(accent_map)
schema = Schema(title=TEXT(analyzer=my_analyzer, spelling=True), titleStemmed = TEXT(analyzer=my_analyzer), 
                content=TEXT(analyzer=my_analyzer,spelling=True), contentStemmed = TEXT(analyzer=my_analyzer),  
                nid=ID(stored=True))

if not os.path.exists("index/index"):
    os.mkdir("index/index")
ix  = create_in("index/index", schema)

