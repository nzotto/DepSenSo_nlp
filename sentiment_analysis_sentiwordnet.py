"""
    Zotto Nicola

    Sentiment analysis using SentiWordNet
"""

## import nltk
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
## import from lemmatize_wordnet.py
from lemmatize_wordnet import get_wordnet_pos


def SentiWordnet_analysis(lemmatized_tokens):
    """
    Sentiment analysis using SentiWordnet.
    0 meaning neutral, greater than 0 positive and lesser than 0 negative.
    
    :param lemmatized_tokens: a list of str, preprocesed tokens
    :return: float, the sentiment score.
    """
    sentiment = 0.0
    tokens_count = 0

    ## part of speech tagging of the tokens
    pos = nltk.pos_tag(lemmatized_tokens)

    for token in pos:
        word = token[0]
        tag = get_wordnet_pos(token[1])
        ## look for the token in Wordnet
        synsets = wn.synsets(word, pos=tag)
        if not synsets:
            continue
        ## take the first sense, the most common
        synset = synsets[0]
        swn_synset = swn.senti_synset(synset.name())
        ## the sentiment is the difference beetween the positive and negative score of the token
        sentiment += swn_synset.pos_score() - swn_synset.neg_score()
        tokens_count += 1

    return sentiment/tokens_count
