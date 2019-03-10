"""
    Nicola Zotto

    Topic modeling using gensim and lda.
"""

## import gensim
import gensim
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
    
def topic_modeling(lemmas):
    """
    Extract topics from document using lda modeling
    :param text: list of str, tokenized and lemmatized tokens
    :return: list of (int, float), topic distribution
    """
    try:
        lda_model = LdaModel.load('data/lda_files/tweetdata.model')
    except EOFError as eofe:
        print(eofe.strerror)
        
    dictionary = gensim.corpora.Dictionary.load('data/lda_files/tweetdata.model.id2word')
    
    ## get bag of word
    bow = dictionary.doc2bow(lemmas)

    ## get document topic
    doc_topic = lda_model.get_document_topics(bow)

    ## formating result as a {topic: proba} dictionary
    res = {}
    for index, prob in sorted(doc_topic, key=lambda var: -1 * var[1]):
        ## res.append("Probability: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))
        res[lda_model.print_topic(index, 5)] = prob
    return res
    
