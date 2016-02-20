from __future__ import division
import math
from creeper_pp.user import User

class InformationExtractor(object):
    max_statuses = 3200
    page_length = 200

    def __init__(self, api):
        self.api = api

    def extract(self, user_id, max_count):
        user = self.api.get_user(user_id)
        followers_count = user.followers_count
        following_count = user.friends_count
        total_tweets = user.statuses_count
        statuses_count = min(user.statuses_count, self.max_statuses, max_count)
        pages_count = int(math.ceil(statuses_count / self.page_length))
        statuses_text = ""
        mentions_count = 0
        hashtags_count = 0
        urls_count = 0
        retweets_count = 0
        words_count = 0
        for page_num in range(1, pages_count + 1):
            for status in user.timeline(count = min(self.page_length, max_count), page = page_num):
                if status.lang != 'en':
                    continue

                statuses_text += status.text
                mentions_count += len(status.entities['user_mentions'])
                hashtags_count += len(status.entities['hashtags'])
                urls_count += len(status.entities['urls'])
                words_count += len(status.text.split())
                retweets_count += 1 if status.retweeted else 0
        return User(user_id,
                followers_count,
                followers_count,
                total_tweets,
                mentions_count,
                retweets_count,
                hashtags_count,
                urls_count,
                words_count,
                statuses_count,
                statuses_text)
