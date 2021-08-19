# Download Now
This service aims to consolidate API calls to various services to one place. API calls to Crossref, thirdiron and springshare. Service was named **Download Now** because, initially it was intended to produce the full text url of the article only for our download now button for our new website's search function.

<br/>

## Live Demo:
* Click [here](https://dlnow.azurewebsites.net/searchaz?keywords=citation) to search AZ using ```citation``` keyword.
* Click [here](https://dlnow.azurewebsites.net/searchguide?keywords=philippines) to search SMU LibGuides using ```philippines``` keyword.
* Click [here](https://dlnow.azurewebsites.net/geturl?title=The%20Economy%20and%20Demand%20for%20Finance%20Ph.D.S:%201989%E2%80%932001&author=DING,%20David%20K.) to get DOI and Full Text Download link usin:
  * title = ```The Economy and Demand for Finance Ph.D.S: 1989–2001```
  * author = ```DING, David K.```

<br/>

## Local Environment Setup
1. Create local virtual environment and clone the repository
    ```bash
    $ virtualenv --python=python3.5 env                       # local virtual environment
    $ source ./env/bin/activate                               # activate the env; use deactivate to close env
    (env) $ git clone https://github.com/RonBulaon/download-now.git # CLone the repository
    ```
2. if you are using locally uncomment the following line in ```app.py``` bvy removing the '#' comment tag:
    ```python
    #if __name__ == "__main__":                 
        #app.run(host="0.0.0.0", port=80, debug=True) 
    ```
    above code should look like below.
    ```python
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=80, debug=True) 
    ```
3. Change or create ```config.ini``` at the root directory to match new settings or other environment
   ```bash
    [thirdiron]
    ACCESS_TOKEN = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx     # get this from thirdiron
    LIBRARY = xxx                                           # get this from thirdiron

    [guides]
    KEY = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                  # generate this from springshare  
    SITE_ID = xxxx                                          # will be supplied by springshare together with the key

    [az]
    CLIENT_SECRET = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        # generate this from springshare  
    CLIENT_ID = xxx                                         # will be supplied by springshare together with the key
   ```
4. Intall dependencies and run the script.
    ```bash
    (env) $ pip install -r requirements.txt
    (env) $ python app.py                                           # start app
    ```

<br/>

## Usage Notes
* ### /geturl
  * Description : This service uses ***article title*** and ***article author*** to query the DOI from [crossref.org](https://crossref.org/). Once DOI is obtained it will send another query to [ThirdIron.com ](https://thirdiron.com/)to get the full text url of the article. Crossref.org can also provide the link to the article but we want to use Third Iron's because its already linked to our EZ Proxy. 
  <br>

    Query format :
    ```bash
    http://localhost/geturl?title=<article_title>&author=<article_author>
    ```
    
    Sample query :
    * **title** = The Economy and Demand for Finance Ph.D.S: 1989–2001
    * **author** = DING, David K.
    
        ```bash
        http://localhost/geturl?title=The Economy and Demand for Finance Ph.D.S: 1989–2001&author=DING, David K.
        ``` 
        
    Expected result is in json format:
    ```bash
    {
        "authors": "Ding, David K.; Chen, Sheng-Syan",
        "doi": "10.1016/j.ribaf.2003.12.003",
        "title": "The Economy and Demand for Finance Ph.D.S: 1989\u20132001",
        "url": "https://libkey.io/libraries/646/articles/18842023/full-text-file?utm_source=api_62"
    }    
    ```
    You can now use the ```url``` as a link to the fulltext of the article. 
    
    <br>

    **Reference**:
    * [Github](https://github.com/CrossRef/rest-api-doc) repository of crossref.org
    * Sample queires if doing it by hand directly from crossref and thirdiron.
        ```bash
        # Sample 1: 
        https://api.crossref.org/works?query.bibliographic=Overseas+listing+location+and+cost+of+capital+Evidence+from+Chinese+firms+listed+in+Hong+Kong+Singapore+and+the+United+States&query.author=LI
        https://public-api.thirdiron.com/public/v1/libraries/646/articles/doi/10.1080/1540496X.2018.1436436?access_token=<token>

        # Sample 2: 
        https://api.crossref.org/works?query.bibliographic=Are+There+Permanent+Valuation+Gains+to+Overseas+Listing&query.author=Sarkissian
        https://public-api.thirdiron.com/public/v1/libraries/646/articles/doi/10.1093/rfs/hhn003?access_token=<token> 
        ```
        Note : You need a token to make thirdiron work.
<br> 

* ### /searchguide
  * Description : Uses Springshare's APi to query SMU Libraries' [research guides](https://researchguides.smu.edu.sg/). Sample query:
      ```bash
      http://localhost/searchguide?keywords=<keyword>
      ```
      Sample query:
      ```bash
      http://localhost/searchguide?keywords=philippines
      http://localhost/searchguide?keywords=accounting,finance,guide
      ```

      Expected result using ```philippines``` keyword, in json format:
      ```bash
      [{
          "name": "Understanding Philippines",
          "urllink": "https://researchguides.smu.edu.sg/c.php?g=857736",
          "datepublished": "2018-10-11 07:31:23"
      }]
      ```
<br>

* ### /searchaz
  * Description : Uses Springshare's APi to query SMU Libraries' [A-Z Databases](https://researchguides.smu.edu.sg/az.php). Sample query:
    ```bash
    http://localhost/searchaz?keywords=<keyword>
    ```
    Sample query:
    ```bash
    http://localhost/searchaz?keywords=citation
    http://localhost/searchaz?keywords=accounting,finance
    ```

    Expected result using ```citation``` keyword, in json format:
    ```bash
    [{
        "name": "Econlit",
        "urllink": "http://search.ebscohost.com/login.aspx?authtype=ip,uid&profile=ehost&defaultdb=ecn",
        "description": "This database provides citations and abstracts to economic research from 1969. It is produced by the American Economic Association. It includes journal articles, books, collective volume articles, dissertations, working papers and book reviews. Use EconLit to find relevant articles for all fields in economics, such as econometrics, economic forecasting, environmental economics, finance, monetary theory and urban economics. Check the Classification Codes which is useful for EconLit Advanced Search."
    }, 
    {
        "name": "ERIC",
        "urllink": "http://search.ebscohost.com/login.aspx?authtype=ip,uid&profile=ehost&defaultdb=eric",
        "description": "The Educational Resource Information Center (ERIC) provides full text, abstracts or citations of documents and journal articles on education research and practice."
    }, 
    {
        "name": "Index to Legal Periodicals and Books",
        "urllink": "http://search.ebscohost.com/login.aspx?authtype=ip,uid&profile=ehost&defaultdb=lbp",
        "description": "This bibliographic database provides citations of articles from legal periodicals and indexes law books. It covers all areas of jurisprudence, court decisions, legislation, and original scholarship. Data starts from 1981 to present."
    }]
    ```


Note : Springshare does not have an API for searches using a keyword, **searchaz** and **searchguide** are uses string matches in title and description only.
