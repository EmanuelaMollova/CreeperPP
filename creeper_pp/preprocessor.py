from __future__ import division
from collections import Counter

import string
import operator

from nltk import pos_tag
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import bigrams


from creeper_pp.user import User
from tokenizer import tokenizeRawTweetText

class Preprocessor(object):
    def __init__(self, text):
        self.text = text
        self.tokenized = tokenizeRawTweetText(self.text)

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

    def is_ascii(self, s):
        return all(ord(c) < 128 for c in s)

    def remove_stop_words_and_urls(self, no_special = False):
        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['rt', 'RT', 'via', 'i']
        terms = [token for token in self.tokenized if ((token not in stop) and ("http" not in token) and ("'" not in token) and self.is_ascii(token))]
        if(no_special):
            terms = [term for term in terms if not term.startswith('#') and not term.startswith('@') and term.isalpha()]

        terms = [term.lower() for term in terms]
        terms = [token for token in terms if ((token not in stopwords.words('english')))]

        return terms


    def vader(self):
        sid = SentimentIntensityAnalyzer()
        results = {'neg': 0.0, 'pos': 0.0, 'neu': 0.0, 'compound': 0.0}
        ss = sid.polarity_scores(self.text)
        for k in sorted(ss):
            results[k] += ss[k]

        return results

    def most_used_words(self, max_count = 5):
        count_all = Counter()
        filtered_terms = self.remove_stop_words_and_urls(True)
        terms_all = [term for term in self.remove_stop_words_and_urls(True) if not term.startswith('@')]
        count_all.update(terms_all)

        return count_all.most_common(max_count)

    def most_used_hashtags(self, max_count = 5):
        count_all = Counter()
        terms_all = [term for term in self.remove_stop_words_and_urls() if term.startswith('#')]
        count_all.update(terms_all)

        return count_all.most_common(max_count)

    def most_used_bigrams(self, max_count):
        count_all = Counter()
        terms_all = [term for term in bigrams(self.remove_stop_words_and_urls(True))]
        count_all.update(terms_all)

        return count_all.most_common(max_count)
