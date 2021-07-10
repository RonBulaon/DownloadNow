from flask import Flask
from flask import request

from fulltextURL import *
from searchGuide import *
from searchAZ import *

app = Flask(__name__)

@app.route("/")
def usageDetails():
    return "Please visit https://github.com/RonBulaon/download-now usage instructions!"

@app.route("/geturl")
def getURL():
    title = request.args.get('title')
    author = request.args.get('author')

    if title and author:
        data = resolveURL(title,author)
        return data
    else:
        return {'error':'missing values'}


@app.route("/searchguide")
def searchGuide():
    keywords = request.args.get('keywords')

    if keywords:
        data = checkGuide(keywords)
        return data
    else:
        return {'error':'missing values'}


@app.route("/searchaz")
def searchAZ():
    keywords = request.args.get('keywords')

    if keywords:
        data = checkAZ(keywords)
        return data
    else:
        return {'error':'missing values'}

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=80, debug=True) 
    
