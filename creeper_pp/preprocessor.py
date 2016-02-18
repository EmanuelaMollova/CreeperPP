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
    def __init__(self, textList):
        self.textList = textList
        self.text = ''.join(textList)
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
        stop = stopwords.words('english') + punctuation + ['rt', 'RT', 'via']
        terms = [token for token in self.tokenized if token not in stop and "http" not in token and self.is_ascii(token)]
        if(no_special):
            terms = [term for term in terms if not term.startswith('#') and not term.startswith('@')]

        return terms


    def vader(self):
        sid = SentimentIntensityAnalyzer()
        results = {'neg': 0.0, 'pos': 0.0, 'neu': 0.0, 'compound': 0.0}
        for sentence in self.textList:
            ss = sid.polarity_scores(sentence)
            for k in sorted(ss):
                results[k] += ss[k]

        for k in sorted(results):
            results[k] = results[k] / len(self.textList)

        return results

    def most_used_words(self):
        count_all = Counter()
        terms_all = [term for term in self.remove_stop_words_and_urls() if not term.startswith('@')]
        count_all.update(terms_all)

        return count_all.most_common(5)

    def most_used_hashtags(self):
        count_all = Counter()
        terms_all = [term for term in self.remove_stop_words_and_urls() if term.startswith('#')]
        count_all.update(terms_all)

        return count_all.most_common(5)

    def most_used_bigrams(self):
        count_all = Counter()
        terms_all = [term for term in bigrams(self.remove_stop_words_and_urls(True))]
        count_all.update(terms_all)

        return count_all.most_common(5)
