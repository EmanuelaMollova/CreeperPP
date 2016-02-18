from __future__ import division

import string

from nltk import pos_tag
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from creeper_pp.user import User
from tokenizer import tokenizeRawTweetText

class Preprocessor(object):
    def __init__(self, text):
        self.text = text
        self.tokenized = tokenizeRawTweetText(text)

    def tokenize(self):
        return tokenizeRawTweetText(self.text)

    def stem(self):
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in self.tokenized]

    def lemmatize(self):
        lemmatiser = WordNetLemmatizer()
        return [lemmatiser.lemmatize(token) for token in self.tokenized]

    def pos(self):
        return pos_tag(self.tokenized)

    def remove_stop_words_and_urls(self):
        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['rt', 'via']
        return [token for token in self.tokenized if token not in stop and "http" not in token]

    def vader(self):
        sid = SentimentIntensityAnalyzer()

        ss = sid.polarity_scores(self.text)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]))
        print()

        # sentences = ["VADER is smart, handsome, and funny.", # positive sentence example
        #     "VADER is smart, handsome, and funny!", # punctuation emphasis handled correctly (sentiment intensity adjusted)
        #     "VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
        #     "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
        #     "VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
        #     "VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!",# booster words & punctuation make this close to ceiling for score
        #     "The book was good.",         # positive sentence
        #     "The book was kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
        #     "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
        #     "A really bad, horrible book.",       # negative sentence with booster words
        #     "At least it isn't a horrible book.", # negated negative sentence with contraction
        #     ":) and :D",     # emoticons handled
        #     "",              # an empty string is correctly handled
        #     "Today sux",     #  negative slang handled
        #     "Today sux!",    #  negative slang with punctuation emphasis handled
        #     "Today SUX!",    #  negative slang with capitalization emphasis
        #     "Today kinda sux! But I'll get by, lol" # mixed sentiment example with slang and constrastive conjunction "but"
        # ]

        # for sentence in sentences:
        #     print(sentence)
        #     ss = sid.polarity_scores(sentence)
        #     for k in sorted(ss):
        #         print('{0}: {1}, '.format(k, ss[k]))
        #     print()
