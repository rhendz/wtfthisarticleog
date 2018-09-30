from bs4 import BeautifulSoup
from gsearch.googlesearch import search
from newspaper import Article
import datetime
import json
from jsonmerge import merge
import nltk
import os
import re
import requests

# Set ENV_VAR for Google API Creds.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="wtfthisarticle5-a3a6272bf9a1.json"
## nltk.download('punkt')

# Custom scripts
from modules.summarize import *
from modules.sentiment import *

## Useful for extracting author if newspaper fails
AUTHOR_REGEX = re.compile('(author)|(byline)', re.I) # Ignore case

article_data = {
    'title': -1,
    'author': -1,
    'publish_date': -1,
    'img_src': -1,
    'text': -1
}

# This fnc has a much higher success rate at finding the author
def getAuthor(article):
    # Must turn article into a soup obj
    soupObj = BeautifulSoup(article.html, 'html.parser')

    # Returns first occurrence of matched AUTHOR_REGEX
    matched_expr = soupObj.find('', {'class' : AUTHOR_REGEX})

    # Try itemprop
    if matched_expr is None:
        matched_expr = soupObj.find('', {'itemprop' : AUTHOR_REGEX})

    # Try href
    if matched_expr is None:
        matched_expr = soupObj.find('', {'href' : re.compile('profile', re.I)})

    # Nothing left to check, returns
    if matched_expr is None:
        return -1

    # Find firstmost child
    while matched_expr.findChild() is not None:
        matched_expr = matched_expr.findChild()

    if matched_expr is not None:
        return re.sub(r'By ', '', matched_expr.get_text())
    else:
        return -1

def getInitJSON(Url):
    ## BEGIN BUILDING INITIAL ARTICLE
    article = Article(Url) # Instantiate article
    article.download() # Required
    article.parse() # Required

    title = article.title
    # for counter, _ in enumerate (title[::-1]):
    #     if (title[counter] == '-'):
    #         title = title[:counter]
    #         break

    author_head = article.authors ## Sometimes this fnc. does not work
    if len(author_head) == 0:
        author_head = getAuthor(article) # Try again w my fnc
    else:
        author_head = article.authors[0]

    publish_date = article.publish_date
    img_src = article.top_image
    summary = article.summary.strip()
    text = article.text.strip()
    summary = summarize(text)

    try:
        article_data['title'] = title
        article_data['author'] = author_head
        # datetime objs are not serializable
        article_data['publish_date'] = publish_date.strftime("%Y-%m-%d")
        article_data['img_src'] = img_src
        article_data['text'] = text
    except AttributeError:
        pass # This is fine
    ## END BUILDING INITIAL ARTICLE

    with open('modules/json/init.json', 'w') as outfile:
        json.dump(article_data, outfile)

    if text is not None or text != '':
        summarize(text)

    # Sentiment analysis
    analyze(text)

    ## Search google for related articles/links
    json_results = {}
    results = search(title, num_results=4)
    for result in results:
        json_results.update({result[0] : result[1]})

    with open('modules/json/relatedLinks.json', 'a') as outfile:
        json.dump(json_results, outfile)

    bigJSON = {}

    ## with open('modules/json/relatedLinks.json', 'r') as outfile:
    bigJSON = merge(bigJSON, json_results)

    with open('modules/json/init.json', 'r') as outfile:
        bigJSON = merge(bigJSON, json.load(outfile))

    with open('modules/json/summary.json', 'r') as outfile:
        bigJSON = merge(bigJSON, json.load(outfile))

    with open('modules/json/sentiment.json', 'r') as outfile:
        bigJSON = merge(bigJSON, json.load(outfile))

    print(bigJSON)

    with open('modules/json/bigJSON.json', 'w') as outfile:
        json.dump(bigJSON, outfile)
