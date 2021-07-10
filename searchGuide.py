import requests
import time
import json
import os
from re import search
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

KEY = config['guides']['KEY']
SITE_ID = config['guides']['SITE_ID']
URL = 'https://lgapi-au.libapps.com/1.1/guides?site_id='+SITE_ID+'&key='+KEY+'&sort_by=relevance&expand=pages&status=1'
data = ''

def checkGuide(keyword):
    global URL, data
    results_index = []
    resultsData = ''
    keywords = keyword.split(',')
    for i in range(0,len(keywords)):
        keywords[i] = keywords[i].lower() 

    data = requests.get(URL,timeout=60)
    jsonData = data.content.decode("utf-8")
    data = json.loads(jsonData)

    for count in range (0, int(len(data))):
       
        name = data[count]["name"].lower()
        description = data[count]["description"].lower()

        for keyword in keywords:
            if (search(keyword, description) or search(keyword, description)):
                results_index.append(count)
                if resultsData == '':
                    resultsData =  str('{"name":"%s","urllink":"%s","datepublished":"%s"}' % (data[count]["name"], data[count]["url"],data[count]["published"]))
                else:
                    resultsData =  resultsData + str(',{"name":"%s","urllink":"%s","datepublished":"%s"}' % (data[count]["name"],data[count]["url"],data[count]["published"]))
                    
    resultsData = '['+ resultsData +']'

    return resultsData