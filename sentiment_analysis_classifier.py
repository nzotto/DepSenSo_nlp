# -*- coding: utf-8 -*-
"""
    Nicola Zotto

    Sentiment analysis using tweet database.
"""
## preprocess text
import demojize_text as dt
import lemmatize_wordnet as lm
import tokenizer_userMentionsCount as tk
## database
import json
import pandas as pd
## sklearn
from sklearn import tree
from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

def preprocess_text(text):
    """
    """
    demojized_text = dt.demojize(text)
    tokens, userMentions = tk.tokenize(text,"twitter")
    lematized_tokens = lm.lemmatize(tokens)
    processed_text = ' '.join(lematized_tokens)
    return processed_text

def import_tweetdata():
    '''
    import tweet data to be fitted into a calssifier!
    :return: x: A list, the preprocessed text from tweetdata.txt
             y: A list, the sentiment values associated with the tweets from tweetdata.txt
             trainTxt: A list of str, the preprocessed text from tweetdata.txt for training
             testTxt: A list of str, the preprocessed text from tweetdata.txt for testing
             trainSent: A list of int, the sentiment values associated with the tweets from tweetdata.txt for trainTxt
             testSent: A list of int, the sentiment values associated with the tweets from tweetdata.txt for testTxt
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
    ## sentiment and tweet database.
    l = len(tweets_data)
    x = []
    y = []
    for i in range(l):
        if tweets_data[i]['id']==sent['id'][i]:
            x.append(preprocess_text(tweets_data[i]['text']))
            y.append(sent['sentiment'][i])
    trainTxt, testTxt, trainSent, testSent = train_test_split(x, y, test_size=0.25, random_state=None)
    return trainTxt, testTxt, trainSent, testSent

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

def initialize_naibeBayes(vectorizer, tweetdataText, tweetdataSentiment):
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

def initialize_ridge(vectorizer, tweetdataText, tweetdataSentiment):
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

def initialize_logisticRegression(vectorizer, tweetdataText, tweetdataSentiment):
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

def initialize_supportVectorMachine(vectorizer, tweetdataText, tweetdataSentiment):
    """
    :param vectorizer: a text vectorizer
    :param tweetdataText: A list initialized in import_tweetdata
    :param tweetdataSentiment: A list initialized in import_tweetdata
    :return: a trained svm classifier.
    """
    train_features = vectorizer.fit_transform(tweetdataText)
    lsvm = LinearSVC()
    lsvm.fit(train_features, [int(r) for r in tweetdataSentiment])
    return lsvm

def initialize_decisionTree(vectorizer, tweetdataText, tweetdataSentiment):
    """
    :param vectorizer: a text vectorizer
    :param tweetdataText: A list initialized in import_tweetdata
    :param tweetdataSentiment: A list initialized in import_tweetdata
    :return: a trained decision tree classifier.
    """
    train_features = vectorizer.fit_transform(tweetdataText)
    dtc = tree.DecisionTreeClassifier()
    dtc.fit(train_features, [int(r) for r in tweetdataSentiment])
    return dtc

def score_classifier(clas, vect, testTxt, testSent):
    """
    return the accuracy score of a trained classifier on a test set
    :param clas: a trained classifier
    :param vect: a text vectorizer
    :param tweetdataText: A test set initialized in import_tweetdata, the texttual part of the sent
    :param tweetdataSentiment: A list initialized in import_tweetdata, the sentiment score part of the set
    """
    tmp = vect.fit_transform(testTxt)
    score = clas.score(tmp, [int(r) for r in testSent])
    return score
        
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
    
