# -*- coding: utf-8 -*-
"""
    Nicola Zotto

    Sentiment analysis using tweet database.
"""
## database
import json
import pandas as pd
## sklearn
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

def innitialisation_classifier():
    """

    :return: a trained naive_bayes classifier and a vectorizer for text.
    """
    ## import tweet data into an array.
    tweets_data_path = 'data/tweetdata.txt'
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue

    ## import labeled sentiments.
    sent = pd.read_excel('data/sentiment2.xlsx')

    ## fuze together sentiment and tweet database.
    x = []
    y = []
    for i in range(len(tweets_data)):
        if tweets_data[i]['id']==sent['id'][i]:
            x.append(tweets_data[i]['text'])
            y.append(sent['sentiment'][i])

    ## machine learning.
    vectorizer = CountVectorizer(stop_words='english')

    train_features = vectorizer.fit_transform(x)
    nb = MultinomialNB()
    nb.fit(train_features, [int(r) for r in y])

    return nb, vectorizer

def sentiment_analysis(text, clas, vect):
    """

    :param text: a list of strings or a single string to be classified
    :param clas: a trained classifier for sentiment analysis
    :param vect: a text vectorizer
    :return: a list of tuples such as (text, prediction) with a polarity of 1 bing positive, 0 neutral and -1 negative.
    """
    assert type(text) is list or type(text) is str
    res=[]
    if type(text) is list:
        for t in text:
            res.append((t, clas.predict(vect.transform([t]))[0]))
    else:
        res.append((text, clas.predict(vect.transform([text]))[0]))
    return res
    

if __name__ == '__main__': main()
