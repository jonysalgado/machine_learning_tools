#-------------------------------------------------------------------------------
# importation
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer
import re
import string
import numpy as np


#-------------------------------------------------------------------------------
# Class NLP_tools

class NLP_tools:
    def __init__(self, language = "english"):
        self.tweet_tools = tweet_tools(language)


#-------------------------------------------------------------------------------
# Class NLP_base

class NLP_base:
    def __init__(self, language):
        pass


#-------------------------------------------------------------------------------
# Class tweet_tools

class tweet_tools(NLP_base):
    def __init__(self, language):
        super().__init__(language)
        # TODO: check if the language is corect and suggest posible languages
        self.stopwords = stopwords.words(language)

    def process_tweet(self, tweet: str) -> list:
        """ 
        Process tweet to NLP models.

        This function transform tweet string in list of 
        stemmed words alread processed to NLP models.

        Parameters
        ----------
        tweet : str
            A tweet string.

        Returns
        -------
        list
            List of stemmed words to NLP models.
        """
        tweet = re.sub(r'^RT[\s]+', '', tweet)
        tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
        tweet = re.sub(r'#', '', tweet)
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                                reduce_len=True)
        tweet = tokenizer.tokenize(tweet)
        tweets_clean = []

        for word in tweet: # Go through every word in your tokens list
            if (word not in self.stopwords and  # remove stopwords
                word not in string.punctuation):  # remove punctuation
                tweets_clean.append(word)

        stemmer = PorterStemmer() 
        tweets_stem = [] 

        for word in tweets_clean:
            stem_word = stemmer.stem(word)  # stemming word
            tweets_stem.append(stem_word)  # append to the list
        
        return tweets_stem    

    def build_freqs(self, tweets: list, ys: np.ndarray) -> dict:
        """ 
        Build a dictionary with words and frequences to all labels that
        they appear in the tweets.

        Parameters
        ----------
        tweets : list
            List of tweets like string.

        ys: numpy.ndarray
            Numpy array with label for all the tweets ordered.

        Returns
        -------
        dict
            Dictionary with word and label as key and frequences as value.
        """

        freqs = {}
        yslist = np.squeeze(ys).tolist()

        for y, tweet in zip(yslist, tweets):
            for word in self.process_tweet(tweet):
                pair = (word, y)
                freqs[pair] = freqs.get(pair, 0) + 1

        return freqs
    


