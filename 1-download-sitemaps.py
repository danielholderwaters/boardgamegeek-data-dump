import BeautifulSoup #BeautifulSoup4 is the most recent version
from httplib2 import Http
import os
#adding the following import lines
import sys
import datetime

http = Http()

if len(sys.argv) > 1:
    DATE_DIR = sys.argv[1]
else:
    DATE_DIR = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m") #adding the .datetime function between datetime and .strftime

DUMP_DIR = os.path.join("BoardGameGeek.xml", DATE_DIR)
SITEMAP_DIRECTORY = os.path.join(DUMP_DIR, "maps")
#following if statement creates the file BGG xml directory within the current working directory.
if not os.path.exists(SITEMAP_DIRECTORY):
    os.makedirs(SITEMAP_DIRECTORY)

def req(*args, **kwargs):
    try:
        response, body = http.request(*args, **kwargs)
    except Exception as e: #changing the syntax on this line
        print ("Could not request %r %r: %s" % (args, kwargs, e)) #surrounding the print statement in parentheses
        return None, None
    return response, body

response, body = req('http://boardgamegeek.com/sitemapindex')
import time

soup = BeautifulSoup(body, "lxml")
quest = soup.find_all("loc")
print(type(quest))

for loc in soup.find_all("loc"):
    url = loc.string.strip()
    filename = url[url.rindex("sitemap_")+len("sitemap_"):]
    path = os.path.join(SITEMAP_DIRECTORY, filename)
    if os.path.exists(path):
        continue
    print ("%s -> %s" % (url, path)) #added parenthases to the print command
    response, body = req(url)
    open(path, "w").write(str(body)) #some of the pages were throwing back errors because they were "bytes" and not "str", adding the str() command ensures th
    time.sleep(.1) #reduced this to .1 because...I wanted the program to run faster
