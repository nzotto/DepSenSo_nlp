#!/usr/bin/python
# -*- encoding: utf-8 -*-

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import json

from collections import defaultdict

## import nltk
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer


def tokenize(text):
    """
    tokenize text and removes user handles (@user_name), long words ("loooong"="looong") and removes uppercases
    :param text: str, a string to be tokenized
    :return: list of str, the tokens 
    """
    tknzr = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    return tknzr.tokenize(text)

def lemmatize(list_of_tokens):
    """
    """
    lemmatizer = WordNetLemmatizer()
    res=[]
    for tokens in list_of_tokens:
        lemmatized = []
        for t in tokens:
            lemmatized.append(lemmatizer.lemmatize(t))
        res.append(lemmatized)
    return res

def filter_stopwords(list_of_tokens):
    """
    """
    res=[]
    for tokens in list_of_tokens:
        filtered_tokens = []
        for t in tokens:
            if t not in STOPWORDS and len(t) > 3 and t.isalpha():
                filtered_tokens.append(t)
        res.append(filtered_tokens)
    return res
    
#creates a dictionary and a bag of words for LDA
def create_bow(lemmatized_data):
    print('creating bow')
    dictionary = gensim.corpora.Dictionary(lemmatized_data)
    corpus = [dictionary.doc2bow(token) for token in lemmatized_data]
    return dictionary, corpus


def main():
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

    ## preprocessing
    tokens = []
    for tweet in tweets_data:
        temp = tokenize(tweet["text"])
        tokens.append(temp)

    tokens = filter_stopwords(tokens)
    tokens = lemmatize(tokens)
    
    id2word, corpus = create_bow(tokens)

    ## lda model training
    lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=20, update_every=1, chunksize=100, passes=5, per_word_topics=True)

    lda_model.save('data/lda_files/tweetdata.model')


if __name__ == "__main__": main()
