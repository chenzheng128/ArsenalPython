#coding: utf-8
import pymongo
from pymongo import MongoClient
from datetime import datetime

import logging
log = logging.getLogger(__name__)

class StorageClient(object):
    def __init__(self):
        #default client localhost interface on port 27017.
        self.client = MongoClient() # MongoClient("mongodb://mongodb0.example.net:27019")
        self.db = MongoClient().test
        self.db_movie = MongoClient().douban_movie
        pass

    def save_movie_in_theaters(self, data={"test":"true"}):
        result = self._save(self.db.movie_in_theaters, data)
        if result!=None: log.debug( "insert movie_in_theaters id: %s" % result.inserted_id)
        return result
    def save_movie_top250(self, data={"test":"true"}):
        result = self._save(self.db.movie_top250, data)
        if result!=None: log.debug( "insert movie_top250 id: %s" % result.inserted_id)
        return result
    def save_movie_coming_soon(self, data={"test":"true"}):
        result = self._save(self.db.movie_coming_soon, data)
        if result!=None: log.debug( "insert movie_coming_soon id: %s" % result.inserted_id)
        return result
    def save_movie_us_box(self, data={"test":"true"}):
        result = self._save(self.db.movie_us_box, data)
        if result!=None: log.debug( "insert movie_us_box id: %s" % result.inserted_id)
        return result
    def save_movie_weekly(self, data={"test":"true"}):
        result = self._save(self.db.movie_weekly, data)
        if result!=None: log.debug( "insert movie_weekly id: %s" % result.inserted_id)
        return result
    def save_movie_new_movies(self, data={"test":"true"}):
        result = self._save(self.db.movie_new_movies, data)
        if result!=None: log.debug( "insert movie_new_movies id: %s" % result.inserted_id)
        return result

    def save_movie_subject(self, id, data):
        """
        追踪电影变化信息, 每个电影存在db_movie数据库的独立的collection下面
        :param id:
        :param data:
        :return:
        """
        result = self._save( self.db.get_collection("movie__id_%s" % id), data )
        if result!=None: log.debug( "insert movie_id_%s id: %s" % (id, result.inserted_id))
        return result
    def collect_movie_subject(self, id, data):
        """
        保持电影信息, 所有电影存放在一个 collection movie_subject 下
        :param id:
        :param data:
        :return:
        """
        result = self.db.get_collection("movie_subjects").findOneAndReplace({"id":id},  data)

        if result!=None: log.debug( "insert movie_subjects id: %s" % result.inserted_id)
        return result

    def _save(self, table, content):
        if content != None:
            #print now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%s"), content
            #插入抓取时间标签
            content["timestamp"] = datetime.now().strftime("%s")
            content["timestr"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return table.insert_one(content)
        else:
            log.warn("!!!content is None, pleasing checking..")
            return None

    def get_movies_subject_ids(self, collects):
        """
        从 mongodb collects 中获取不重复的id列表, 便于下一次抓取
        :return:
        """
        ids = set()
        for collect in collects:
            cursor = collect.find().sort([("_id", pymongo.DESCENDING)]).limit(1)
            for result in cursor:
                for subject in result["subjects"]:
                    #print type(subject)
                    if subject.has_key("subject"):
                        subject = subject["subject"]
                    ids.add(subject["id"])
            log.debug("plus ids  from collects %s length %s  " % ( collect, len(ids) ))
        return ids

    def get_movies_subject_ids_all(self):
        return self.get_movies_subject_ids([self.db.movie_coming_soon, self.db.movie_in_theaters , self.db.movie_us_box, self.db.movie_top250])

    def get_movies_subject_ids_recent(self):
        return self.get_movies_subject_ids([self.db.movie_coming_soon, self.db.movie_in_theaters])

    def get_movies_subject_ids_in_theaters(self):
        return self.get_movies_subject_ids([ self.db.movie_in_theaters])


if __name__ == "__main__":
    level = logging.WARNING
    level = logging.DEBUG
    logging.basicConfig(format='%(name)s \t\t%(levelname)-8s %(filename)8s %(funcName)8s() [%(message)-60s] %(module)s',
                        level=level)
    storage_client = StorageClient()
    # storage_client.save_movie_in_theaters()
    #ids = storage_client.get_movies_subject_ids_recent()
    #print len(ids), ids
    #ids = storage_client.get_movies_subject_ids_in_theaters()
    #print len(ids), ids
    id = "26614128"
    storage_client.collect_movie_subject(id, {"id":id, "hello":"true"})
