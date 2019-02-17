# DepSenSo_nlp
Natural Language Processing part of the depsenso project

## Preprocessing

### demojize_text.py
__Libraries__: emoji
Converts all emojis in the passed string in text format (i.e. :emoji_name:)
This allows us to transform emojies into key words that are usefull for sentiment analysis. For example, "\U0001f642" is :slightly_smiling_face:

### tokenizer_userMentionsCount.py
__Libraries__: nltk, sys, unicodedata and string
Tokenizes text using TweetTokenizer (from nltk). In order to prepare the text for further analysis, we remove user handles (using the format of reddit or twitter), capitalization, hyperlinks and punctuation.
Additionaly, tweet tokenizer normalizes long-words by maximizing the number of reapeated characters to 3 ("lloooooonnnnnnng" -> "llooonnng") and we counts every distinct user_mention to prepare for the network analysis of the user.

### lemmatize_wordnet.py
__Libraries__: nltk
Lematizes a list of tokens using the WordNetLemmatizer. The correct lemma is chosen using the pos tag of each token.

## Training

### train_model_lda_tweetdata.py
One time use code to train our lda classifier using the twitter data available at https://github.com/AshwanthRamji/Depression-Sentiment-Analysis-with-Twitter-Data
This code isn't to be used on the actuall application DepSenSo

## Topic Modeling

### topic_modeling_lda.py
__Libraries__: gensim
Using the trained classifier find the most likely topics from a list of lemmatized tokens. The result is a python dictionary in the form {topic : probability}.

### topic_modeling_empath.py
__Libraries__: empath
Returns the repartition of lexical categories, similarly to LIWC. For the purpose of DepSenSo we define three custom categories: Depression, Mental_health and Anxiety.

## Sentiment Analysis
We determine sentiment polarity as 0 meaning neutral, greater than 0 positive and lesser than 0 negative.

### sentiment_analysis_classifier.py
__Libraries__: json, pandas and slearn
After creating a naive_bayes classifier using the twitter data available at https://github.com/AshwanthRamji/Depression-Sentiment-Analysis-with-Twitter-Data. We can calsculate the polarity of a string or a list of strings.


### sentiment_analysis_sentiwordnet.py
__Libraries__: nltk and lemmatize_wordnet.py
Using sentiWordnet, we calculate the polarity of a text as the sum of the polarity of every lematized token.

## Data Collection
At present we are able to get data from reddit.com and twitter.com. Both site use OAuth2 for identification of third party application using their data. As such we need accounts for both sites.

### get_tweets_from_specified_account.py
__Libraries__: tweetpy and datetime
Import Twitter data from a specified accound. After connecting to twitter using out application credential we can pull the complette history of a twitter user provided we know his username.


### get_reddit_from_specified_account.py
__Libraries__: praw
Import reddit data from a specified accound. After connecting to reddit using out application credential we can pull the last 1000 submitions and comments of a reddit user provided we know his username. 
The 1000 limit is hardcoded in the praw library.
