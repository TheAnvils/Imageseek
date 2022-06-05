from serpapi import GoogleSearch
import os
from dominate import document
from dominate.tags import *
from flask import *
app = Flask('app')
apikey = input("api key: ")
image_results = []
val = input("query: ")
for query in [val]:
    params = {
        "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
        "q": query,                       # search query
        "tbm": "isch",                    # image results
        "num": "10",                     # number of images per page
        "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
        "api_key": apikey,   # your serpapi api key
      "gl": "es"
    }

    search = GoogleSearch(params)         # where data extraction happens

    images_is_present = True
    while images_is_present:
        results = search.get_dict()       # JSON -> Python dictionary

        # checks for "Google hasn't returned any results for this query."
        if "error" not in results:
            for image in results["images_results"]:
                if image["original"] not in image_results:
                    print(image["original"])
                    image_results.append(image["original"])
            
            # update to the next page
            break;
        else:
            images_is_present = False
            print(results["error"])

photos = image_results

with document(title='Search results') as doc:
    h1('Search results')
    for path in photos:
        div(img(src=path), _class='photo')
    style("""\
         div {
            zoom: 0.5;
         }
     """)
htmlcontents = doc.render()
@app.route('/')
def index():
  return htmlcontents
app.run(host='0.0.0.0', port=8080)