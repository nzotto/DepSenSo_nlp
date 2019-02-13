"""
    Zotto Nicola

    Lexical categories analysis using empath
"""

from empath import Empath

def create_lexicon():
    """
    Create and define desired categories for an exmpath lexicon
    :return: an Empath lexicon
    """
    lexicon = Empath()
    ## create appropriate categories
    lexicon.create_category("Depression",["depression"],model="reddit")
    lexicon.create_category("Mental_health",["mental_health"],model="reddit")
    lexicon.create_category("Anxiety",["anxiety"],model="reddit")
    return lexicon

def analyze_empath(texts,lexicon):
    """
    Analyzes given tweet or list of tweets and returns the analysis
    :param tweets: tweets to be analyzed
	:param lexicon: an Empath lexicon
    :return: anlysis result
    """
    if (type(texts) is not list and type(texts) is not str) or texts[0] == "" or len(texts) == 0:
        raise ValueError("texts must be a non-empty string or non-empty list of strings!")
    try:
        ## analysis specific categories
        analysis = lexicon.analyze(texts, categories=["depression","mental_health","suicide"], normalize=True)
        return analysis
    except Exception as e:
        print(e)
