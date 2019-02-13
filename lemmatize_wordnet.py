"""
    Nicola Zotto

    Lematize tokens using WordNet
"""

## import nltk
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

def get_wordnet_pos(treebank_tag):
    """
    Convert pos_tag from treebank to a wordnet position
    
    :param treebank_tag: indicator of type of tag
    :return: wordnet position
    """
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return 'n'

def lemmatize(tokens):
    """
	Lematize tokens using wordnet.
	
    :param tokens: list of str, tokenized document
    :return: list of str, lematized tokens
    """
    lemmatized_tokens = []
    pos = nltk.pos_tag(tokens)
    for token in pos:
            lemmatized_tokens.append(WordNetLemmatizer().lemmatize(token[0], get_wordnet_pos(token[1])))
    return lemmatized_tokens
