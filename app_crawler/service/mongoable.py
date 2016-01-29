import pymongo

instance = None


class Mongoable(object):
  def __init__(self, *a, **kw):
    self.mongo_uri = kw.get('mongo_uri')
    self.mongo_db = kw.get('mongo_db')
    self.collection_name = kw.get('mongo_collection')

  def start(self):
    self._client = pymongo.MongoClient(self.mongo_uri)
    self.db = self._client[self.mongo_db]
    self.collection = self.db[self.collection_name]

  def close(self):
    self._client.close()