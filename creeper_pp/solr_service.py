import pysolr
from creeper_pp.user import User

class SolrService(object):
    def __init__(self, core):
        self.conn = pysolr.Solr('http://localhost:8983/solr/' + core, timeout=10)

    def getConnection(self):
        return self.conn

    def getUser(self, user_id):
        results = self.conn.search('id:'+user_id)
        for result in results:
            return result

    def getSimilarUsers(self, user_id, tf=1, df = 1, count = 10):
        similar = self.conn.more_like_this(q='id:'+user_id, mltfl='tweets', **{'mlt.mindf': df, 'mlt.mintf' : tf, 'mlt.count' : count})
        users = []
        for user in similar:
            users.append(user)

        return users

    def getAllUsers(self):
        results = self.conn.search('*:*')
        users = []
        for user in results:
            users.append(user)

        return users


    def addUser(self, userDict):
        toAdd = []
        toAdd.append(userDict)

        self.conn.add(toAdd)
