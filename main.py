
import os
import ConfigParser
from ConfigParser import SafeConfigParser
import shutil
from scraping.Scraping.indexing.buildIndex import build
#crawl over command line


def checkJsonFile(path):
    file = open(path, 'r')
    text = file.read()
    file.close()
    print(text[len(text)-2:len(text)-1])
    if text[len(text)-2] == ',':
        file = open(path, 'w')
        file.write(text[:len(text)-2])
        file.write("]")
        file.close()

#buildIndex
#os.system("script2.py 1")


#copy and count files
# lets create that config file for next time...
cfgPath ="scraping/settings/project.ini"
              
parser = SafeConfigParser()
parser.read(cfgPath)
textsPath = parser.get('general', 'textsPath')
textsPathWeb = parser.get('general', 'textsPathWeb')
pathJson = parser.get('general', 'jsonfiles')
pathOnt = parser.get('general', 'pathOntology' )
indexPath = parser.get('general', 'index')
indexPathWeb = parser.get('general', 'indexWeb')
pathOntWeb = parser.get('general', 'pathontologyWeb')

sections = parser.sections()

blogs = []
language = []
path =  os.path.dirname(__file__) + "scraping/"
#build index


for i in range(1, len(sections)):
    blogs.append(sections[i])
    language.append(int(parser.get(sections[i], 'language')))     
    checkJsonFile(path + pathJson + sections[i] + ".json")

print(blogs)
build(blogs, language, path + textsPath, path + pathJson, path + pathOnt)


#copy files
for section_name in sections:
    try:
        dir = "scraping/" + textsPath + "/" + section_name
        dirWeb = textsPathWeb + "/" + section_name
        lastId = int(parser.get(section_name, "nextId"))
        files = os.listdir(dir)
        print("Files: " + str(len(files)))
        print(lastId)
        parser.set(section_name, 'nextId', str(lastId+len(files)))
        for file in files:
            shutil.move(dir + "/" + file, dirWeb + "/" + file)
                
    except OSError:
        continue
    except ConfigParser.NoOptionError:
        continue

for file in os.listdir("scraping/" + indexPath):
    shutil.copy2("scraping/" + indexPath+ "/" + file, indexPathWeb + "/" + file)
    
for file in os.listdir("scraping/" + pathOnt):
    try:
        print(pathOntWeb + "/" + file)
        shutil.copy2("scraping/" + pathOnt + file, pathOntWeb + "/" + file)
    except IOError:
        continue

  
with open(cfgPath, "wb") as config_file:
        parser.write(config_file)
        
   
