"""
    Zotto Nicola

    Tokenize text using TweetTokenizer
    Removes stopwords, capitalization, twitter user handles, hyperlinks and punctuation
    Reduces "long words" ie: 'looooooooooooong' => 'looong'
    Counts distinct user mentions.
"""
# import nltk:
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
# impoort string and utilities:
import sys
import unicodedata
from string import punctuation

uc_punctuations = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))

def remove_punctuation(text):
    return text.translate(uc_punctuations)

def tokenize(text,textSrc="other"):
    """
    tokenize text and removes user handles ("@userName"), long words ("loooong"="looong") and removes uppercases
    :param text: str, a string to be tokenized
    :param textSrc: str, the source of the text. Either reddit or twitter
    :return: res: the tokens, a list of str
             userMentions: the users mentioned in the post, list of str
    """
    assert type(text) == str and type(textSrc) == str
    assert textSrc== 'reddit' or textSrc== 'twitter' or textSrc== 'other'
    ## users data
    userMentions = []
    res = []
    ## tokenize
    tknzr = TweetTokenizer(preserve_case=False, strip_handles=False, reduce_len=True)
    tokens = tknzr.tokenize(text)
    for t in tokens:
        ## count user mentions and removes them
        if textSrc=="twitter": ## @userName
            if t.startswith('@') and t not in userMentions:
                userMentions.append(t)
                continue
        if textSrc=="reddit": ## /u/userName
            if t.startswith('/u/') and t not in userMentions:
                userMentions.append(t)
                continue
        ## removes hyperlinks
        if str(t).find('http') != -1:
            continue
        ## removes punctuation                    Variation Selector(\uFE0F)
        if remove_punctuation(t) == "" or t in punctuation or t == '\uFE0F':
            continue
        ## removes stop words
        if t in stopwords.words('english'):
            continue
        res.append(t)
    return res, userMentions
