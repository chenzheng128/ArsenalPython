#coding: utf-8
import pymongo
from pymongo import MongoClient
from datetime import datetime

import logging
log = logging.getLogger(__name__)

class StorageClient(object):
    """
    豆瓣 爬虫的 model 类

    存储 电影 subject 到 subject_recent 下
    存储 变动信息到 move_comoing_soon 下
    """

    def __init__(self):
        #default client localhost interface on port 27017.
        self.client = MongoClient() # MongoClient("mongodb://mongodb0.example.net:27019")
        self.db = MongoClient().test
        self.db_movie = MongoClient().douban_movie
        pass

    def save_movie_in_theaters(self, data={"test_mylib":"true"}):
        result = self._save(self.db.movie_in_theaters, data)
        if result!=None: log.debug( "insert movie_in_theaters id: %s" % result.inserted_id)
        return result
    def save_movie_top250(self, data={"test_mylib":"true"}):
        result = self._save(self.db.movie_top250, data)
        if result!=None: log.debug( "insert movie_top250 id: %s" % result.inserted_id)
        return result
    def save_movie_coming_soon(self, data={"test_mylib":"true"}):
        result = self._save(self.db.movie_coming_soon, data)
        if result!=None: log.debug( "insert movie_coming_soon id: %s" % result.inserted_id)
        return result
    def save_movie_us_box(self, data={"test_mylib":"true"}):
        result = self._save(self.db.movie_us_box, data)
        if result!=None: log.debug( "insert movie_us_box id: %s" % result.inserted_id)
        return result
    def save_movie_weekly(self, data={"test_mylib":"true"}):
        result = self._save(self.db.movie_weekly, data)
        if result!=None: log.debug( "insert movie_weekly id: %s" % result.inserted_id)
        return result
    def save_movie_new_movies(self, data={"test_mylib":"true"}):
        result = self._save(self.db.movie_new_movies, data)
        if result!=None: log.debug( "insert movie_new_movies id: %s" % result.inserted_id)
        return result

    def save_movie_subject(self, id, data):
        """  
        :param id:
        :param data:
        :return:
        """
        # 追踪电影变化信息, 每个电影存在db_movie数据库的独立的collection下面
        if False:  # 不考虑研究影片数据变动， 暂时屏蔽这两个语句， 每个电影作为单独的 collect 数据进行抓取
            result = self._save( self.db.get_collection("movie__id_%s" % id), data )
            if result!=None: log.debug( "insert movie_id_%s id: %s" % (id, result.inserted_id))

        # 另外存储一份到 movie_list 下，便于获取列表数据
        result2 = self._save( self.db.get_collection("subject_recent"), data )
        if result2!=None: log.debug( "insert movie_list id: %s" % (id, result2.inserted_id))
        return result2
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

    def subject_existed(self, col, id):
        """
        检查是否存在相关电影
        """
        result = self.db.get_collection("subject_recent").find({"id":id})
        return result.count() > 0


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
    id = "27191430"  
    id2 = "2719143022"
    # storage_client.collect_movie_subject(id, {"id":id, "hello":"true"})
    print "电影存在"
    print storage_client.subject_existed("subject_recent", id)
    print "电影不存在"
    print storage_client.subject_existed("subject_recent", id2)
