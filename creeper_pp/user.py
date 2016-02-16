class User(object):
    def __init__(self,
            id,
            followers_count,
            following_count,
            total_tweets,
            mentions_count,
            replies_count,
            hashtags_count,
            links_count,
            words_count,
            tweets_count):
        self.id = id
        self.followers_count =  followers_count
        self.following_count =  following_count
        self.total_tweets =  total_tweets
        self.mentions_count  =  mentions_count
        self.replies_count  =  replies_count
        self.hashtags_count  =  hashtags_count
        self.links_count    =  links_count
        self.words_count    =  words_count
        self.tweets_count   =  tweets_count

        @property
        def id(self):
            return self.id

        @property
        def followers_count(self):
            return self.followers_count

        @property
        def total_tweets(self):
            return self.total_tweets

        @property
        def following_count(self):
            return self.following_count

        @property
        def mentions_count(self):
            return self.mentions_count

        @property
        def replies_count(self):
            return self.replies_count

        @property
        def hashtags_count(self):
            return self.hashtags_count

        @property
        def links_count(self):
            return self.links_count

        @property
        def words_count(self):
            return self.words_count

        @property
        def tweets_count(self):
            return self.tweets_count
