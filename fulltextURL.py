import requests
import json
import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ACCESS_TOKEN = config['thirdiron']['ACCESS_TOKEN']
LIBRARY = config['thirdiron']['LIBRARY']

def formatTitle(title):
    y = ''
    for x in title:
        if x == ' ':
            y = y + '+'
        elif x.isalnum():
            y = y + x
    return y

def formatAuthor(author):
    y = author.split(',')[0]
    return y

def checkdoi(title,author):
    z = title
    searchQueryTitle = formatTitle(title)
    searchQueryAuthor = formatAuthor(author)
    url = 'https://api.crossref.org/works?query.bibliographic='+searchQueryTitle+'&query.author='+searchQueryAuthor
    try:
        x = requests.get(url,timeout=60)
    except:
        return -1
    else:
        x = json.loads(x.content)
        resultCount = int(x['message']['items-per-page'])
        for count in range(resultCount):
            if(x['message']['items'][count]['title'][0].lower() == z.lower()):
                return x['message']['items'][count]['title'][0], x['message']['items'][count]['DOI']

    return -2

def getfullTextFile(doi):
    url = 'https://public-api.thirdiron.com/public/v1/libraries/'+LIBRARY+'/articles/doi/'+doi+'?access_token='+ACCESS_TOKEN 
    x = requests.get(url,timeout=60)
    try:
        x = json.loads(x.content)
    except:
        return -3
    else:
        return x['data']['title'],x['data']['fullTextFile'],x['data']['authors']


def resolveURL(title,author):
    title1,doi = checkdoi(title,author)
    title2, url, authors = getfullTextFile(doi)
    if title1 == title2:
        data = {
                'title':title, 
                'doi':doi, 
                'authors':authors, 
                'url':url
        }
        
        return data
    else:
        return -4

if __name__ == "__main__":
    print(sys.argv[1])
    print(sys.argv[2])
    x = ''
    try:
        x = resolveURL(sys.argv[1],sys.argv[2])
        x = json.dumps(x)
    except:
        print(x)
    else:
        print(x)