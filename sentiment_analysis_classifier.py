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
## persistence
from joblib import dump, load

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

def initialize_classifiers():
    """
Loads all our trained classifiers using joblib's load.
    :return:
    """
    ## load the classifiers
    nb = load('./data/joblib_classifiers/nbOneGrams.joblib')
    nbTwoGrams = load('./data/joblib_classifiers/nbTwoGrams.joblib')
    ridge = load('./data/joblib_classifiers/ridge.joblib')
    lrc = load('./data/joblib_classifiers/lrc.joblib')
    lsvm = load('./data/joblib_classifiers/lsvm.joblib')
    dtc = load('./data/joblib_classifiers/dtc.joblib')
    vectOneGram = load('./data/joblib_classifiers/vectOneG.joblib')
    vectTwoGram = load('./data/joblib_classifiers/vectTwoG.joblib')
    return nb, nbTwoGrams, ridge, lrc, lsvm, dtc, vectOneGram, vectTwoGram

def train_classifiers(tweetdataText, tweetdataSentiment):
    """
Trains 6 classifiers and saves them using joblib's dump.
    :param tweetdataText: A list initialized in import_tweetdata
    :param tweetdataSentiment: A list initialized in import_tweetdata
    """
    ## initialize training features
    oneGramsVectorizer = CountVectorizer(stop_words='english')
    twoGramsVectorizer = CountVectorizer(stop_words='english', ngram_range=(2,2))
    oneGram_train_features = oneGramsVectorizer.fit_transform(tweetdataText)
    twoGram_train_features = twoGramsVectorizer.fit_transform(tweetdataText)
    ## naive bayes with 1 grams
    nb = MultinomialNB()
    nb.fit(oneGram_train_features, [int(r) for r in tweetdataSentiment])
    dump(nb, './data/joblib_classifiers/nbOneGrams.joblib')
    ## naive bayes with 2 grams
    nbTwoG = MultinomialNB()
    nbTwoG.fit(twoGram_train_features, [int(r) for r in tweetdataSentiment])
    dump(nbTwoG, './data/joblib_classifiers/nbTwoGrams.joblib')
    ## ridge
    ridge = RidgeClassifier()
    ridge.fit(oneGram_train_features, [int(r) for r in tweetdataSentiment])
    dump(ridge, './data/joblib_classifiers/ridge.joblib')
    ## logistic regression
    lrc = LogisticRegression()
    lrc.fit(oneGram_train_features, [int(r) for r in tweetdataSentiment])
    dump(lrc, './data/joblib_classifiers/lrc.joblib')
    ## linear support vector machine
    lsvm = LinearSVC()
    lsvm.fit(oneGram_train_features, [int(r) for r in tweetdataSentiment])
    dump(lsvm, './data/joblib_classifiers/lsvm.joblib')
    ## decision tree
    dtc = tree.DecisionTreeClassifier()
    dtc.fit(oneGram_train_features, [int(r) for r in tweetdataSentiment])
    dump(dtc, './data/joblib_classifiers/dtc.joblib')
    ## vectorizers
    dump(oneGramsVectorizer, './data/joblib_classifiers/vectOneG.joblib')
    dump(twoGramsVectorizer, './data/joblib_classifiers/vectTwoG.joblib')

def score_classifier(clas, vect, testTxt, testSent):
    """
    return the classification report of a trained classifier on a test set
    :param clas: a trained classifier
    :param vect: a text vectorizer
    :param tweetdataText: A test set initialized in import_tweetdata, the texttual part of the sent
    :param tweetdataSentiment: A list initialized in import_tweetdata, the sentiment score part of the set
    """
    return classification_report(testSent, clas.predict(vect.transform(testTxt)), digits=4)
        
def sentiment_analysis(text, clas, vect):
    """
    :param text: a single string to be classified
    :param clas: a trained classifier for sentiment analysis
    :param vect: a text vectorizer
    :return: res, the sentiment score such as a polarity of 1 being positive, 0 neutral and -1 negative.
    """
    assert type(text) is str
    res = clas.predict(vect.transform([text]))
    return res[0]
