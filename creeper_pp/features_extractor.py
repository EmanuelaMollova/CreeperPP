from __future__ import division

from creeper_pp.preprocessor import Preprocessor

class FeaturesExtractor(object):
    def __init__(self, user):
        self.user = user
        self.preprocessor = Preprocessor(self.user.tweets_text)

        self.features = []
        self.features.append(user.followers_count)
        self.features.append(user.following_count)
        self.features.append(user.total_tweets)
        self.features.append(user.mentions_count)
        self.features.append(user.replies_count)
        self.features.append(user.hashtags_count)
        self.features.append(user.links_count)
        self.features.append(user.words_count)
        self.features.append(user.tweets_count)

        self.features.append(len(self.preprocessor.remove_stop_words_and_urls()))

        sentiment = self.preprocessor.vader()
        for k in sorted(sentiment):
            self.features.append(sentiment[k])

    def get_features(self):
        return self.features
