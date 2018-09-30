# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import json
import re

def analyze(text):
    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    # print('Text: {}'.format(text))
    # print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

    sentiment = {
        'score' : sentiment.score,
        'magnitude' : sentiment.magnitude
    }
    with open('modules/json/sentiment.json', 'w') as outfile:
        json.dump(sentiment, outfile)
