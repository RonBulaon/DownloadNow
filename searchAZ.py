import requests
import time
import json
import os
from re import search
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

CLIENT_ID = config['az']['CLIENT_ID']
CLIENT_SECRET = config['az']['CLIENT_SECRET']
URL1 = 'https://lgapi-au.libapps.com/1.2/oauth/token'
URL2 = 'https://lgapi-au.libapps.com/1.2/az'
data = ''

def checkAZ(keyword):
    global URL, data
    results_index = []
    resultsData = ''
    keywords = keyword.split(',')
    for i in range(0,len(keywords)):
        keywords[i] = keywords[i].lower() 

    postdata = {
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET,
        'grant_type':'client_credentials'
    }

    try:
        data = requests.post(URL1, data=postdata, timeout=60)
        jsonData = data.content.decode("utf-8")
        authData = json.loads(jsonData)
        access_token = authData['access_token']
    except:
        return { 'error':'authorization failed' }

    if access_token:
        access_token = {'Authorization' : 'Bearer ' + access_token}
        data = requests.get(URL2, headers=access_token, timeout=60)

        data = data.content.decode("utf-8")
        data = json.loads(data)

    for count in range (0, int(len(data))):
       
        name = data[count]["name"].lower()
        description = data[count]["description"].lower()

        for keyword in keywords:
            if (search(keyword, description) or search(keyword, description)):
                results_index.append(count)
                if resultsData == '':
                    resultsData =  str('{"name":"%s","urllink":"%s","description":"%s"}' % (data[count]["name"], data[count]["url"],data[count]["description"]))
                else:
                    resultsData =  resultsData + str(',{"name":"%s","urllink":"%s","description":"%s"}' % (data[count]["name"],data[count]["url"],data[count]["description"]))
                    
    resultsData = '['+ resultsData +']'

    return resultsData