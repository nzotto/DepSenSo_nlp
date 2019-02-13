#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
    Nicola Zotto

    Example of use of every function.
"""
## just for one example
import emoji

## import all our code:
    ## preprosecing text
import demojize_text as dm
import lemmatize_wordnet as lm
import tokenizer_userMentionsCount as tk
    ## sentiment analysis
import sentiment_analysis_classifier as sa_class
import sentiment_analysis_sentiwordnet as sa_swn
    ## topic moideling
import topic_modeling_empath as tm_empath
import topic_modeling_lda as tm_lda

## here's the corpus we want to analyse for this example
from nltk.corpus import webtext

raw_text = webtext.raw(fileids=["singles.txt"])
sent_0 = raw_text[:69]
sentence0AsList = [sent_0] 
#sentence0AsTokens = lematized_tokens[:9]

print("raw text (first hundred char):")
print(raw_text[:100])
print()

## preprocessing:
##demo_text = emoji.emojize('Python is :thumbs_up:')
##demojized_text = dm.demojize(demo_text)
##print("demojized text (different text for lack of emojies):")
##print(emoji.emojize('Python is :thumbs_up:'))
##print('demojized =')
##print(demojized_text)
##print()

tokens, userMentions = tk.tokenize(raw_text,"other")
print("tokens (first 50 tokens):")
print(tokens[:50])
print()
print("number of distinct user mentioned:", userMentions)
print()

lematized_tokens = lm.lemmatize(tokens)
print("lematized tokens (first 50 tokens):")
print(lematized_tokens[:50])
print()

sentence0AsTokens = lematized_tokens[:9] 

## sentiment analysis...
## ... using the classifier:
print("sentiment analysis using the classifier:")
print("-1 = negative, 0 = neutral, 1 = positive")
classifier, vectorizer = sa_class.innitialisation_classifier()
## the clasifier takes a string or list of string as first parameter
score_0 = sa_class.sentiment_analysis(sent_0, classifier, vectorizer)
print("score = ", score_0)
print()

## ... using SentiWordNet:
print("sentiment analysis using SentiWordNet:")
print("-1 = negative, 0 = neutral, 1 = positive")
print(sent_0)
score_0 = sa_swn.SentiWordnet_analysis(sentence0AsTokens)
print("score = ", score_0)
print()

## topic modeling...
## ... using empath:
print()
print()
lexicon = tm_empath.create_lexicon()
print()
print()
print("topic modeling using empath:")
## analyze_empath takes a list of string as parameter
empath_res = tm_empath.analyze_empath(sentence0AsList, lexicon)
print(sent_0)
print("results = ", empath_res)
print()

## ... using lda:
print("topic modeling using lda:")
## topic_modeling takes a list of preprocessed tokens as parameter
lda_res = tm_lda.topic_modeling(sentence0AsTokens)
print(sent_0)
print("results = ")
for i in range(len(lda_res)):
    print(lda_res[i])
print()
