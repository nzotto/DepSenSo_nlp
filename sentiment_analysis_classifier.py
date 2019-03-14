# -*- coding: utf-8 -*-
"""
    Nicola Zotto

    Sentiment analysis using tweet database.
"""
## preprocess text
import lemmatize_wordnet as lm
import tokenizer_userMentionsCount as tk
## database
import json
import pandas as pd
## sklearn
from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

def preprocess_text(text):
    """
    """
    tokens, userMentions = tk.tokenize(text,"other")
    lematized_tokens = lm.lemmatize(tokens)
    processed_text = ' '.join(lematized_tokens)
    return processed_text

def import_tweetdata():
    '''
    import tweet data to be fitted into a calssifier!
    :return: x: A list, the preprocessed text from tweetdata.txt
             y: A list, the sentiment values associated with the tweets from tweetdata.txt
    '''
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
            x.append(preprocess_text(tweets_data[i]['text']))
            y.append(sent['sentiment'][i])
    return x,y

def initialize_vectorizer(n = None):
    """
    :param n: the number of range n-grams used by the vecorizer. Defaults to None
    :return: a text vectorizer
    """
    if n:
        vectorizer = CountVectorizer(stop_words='english', ngram_range=(n,n))
    else:
        vectorizer = CountVectorizer(stop_words='english')
    return vectorizer

def innitialize_naibeBayes(vectorizer, tweetdataText, tweetdataSentiment):
    """
    :param vectorizer: a text vectorizer
    :param tweetdataText: A list initialized in import_tweetdata
    :param tweetdataSentiment: A list initialized in import_tweetdata
    :return: a trained naive_bayes classifier and it's text vectorizer.
    """
    train_features = vectorizer.fit_transform(tweetdataText)
    nb = MultinomialNB()
    nb.fit(train_features, [int(r) for r in tweetdataSentiment])
    return nb

def innitialize_ridge(vectorizer, tweetdataText, tweetdataSentiment):
    """
    :param vectorizer: a text vectorizer
    :param tweetdataText: A list initialized in import_tweetdata
    :param tweetdataSentiment: A list initialized in import_tweetdata
    :return: a trained ridge classifier and it's text vectorizer.
    """
    train_features = vectorizer.fit_transform(tweetdataText)
    ridge = RidgeClassifier()
    ridge.fit(train_features, [int(r) for r in tweetdataSentiment])
    return ridge

def innitialize_logisticRegression(vectorizer, tweetdataText, tweetdataSentiment):
    """
    :param vectorizer: a text vectorizer
    :param tweetdataText: A list initialized in import_tweetdata
    :param tweetdataSentiment: A list initialized in import_tweetdata
    :return: a trained logistic regression classifier.
    """
    train_features = vectorizer.fit_transform(tweetdataText)
    lrc = LogisticRegression()
    lrc.fit(train_features, [int(r) for r in tweetdataSentiment])
    return lrc
    
    
def sentiment_analysis(text, clas, vect):
    """
    :param text: a list of strings or a single string to be classified
    :param clas: a trained classifier for sentiment analysis
    :param vect: a text vectorizer
    :return: res, the sentiment score such as a polarity of 1 being positive, 0 neutral and -1 negative.
    """
    assert type(text) is list or type(text) is str
    res=0
    if type(text) is list:
        for t in text:
            res += clas.predict(vect.transform([preprocess_text(t)]))[0]
    else:
        res = clas.predict(vect.transform([preprocess_text(text)]))[0]
    return res
    
