# coding: utf-8


"""
mongo_demo.py mongodb 的参考持久化代码, 参考官网: https://docs.mongodb.org/getting-started/python/
Source: https://docs.mongodb.org/getting-started/python/
"""
import pymongo
from pymongo import MongoClient
from datetime import datetime

import logging
log = logging.getLogger(__name__)

class StorageClient(object):
    def __init__(self):
        # default client localhost interface on port 27017.
        self.client = MongoClient()  # MongoClient("mongodb://mongodb0.example.net:27019")
        self.db = self.client.test
        pass

    def _save(self):
        result = self.db.restaurants.insert_one(
            {
                "address": {
                    "street": "2 Avenue",
                    "zipcode": "10075",
                    "building": "1480",
                    "coord": [-73.9557413, 40.7720266]
                },
                "borough": "Manhattan",
                "cuisine": "Italian",
                "grades": [
                    {
                        "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                        "grade": "A",
                        "score": 11
                    },
                    {
                        "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                        "grade": "B",
                        "score": 17
                    }
                ],
                "name": "Vella",
                "restaurant_id": "41704620"
            }
        )
        print "insert restaurants id: ", result.inserted_id

    def _find(self):
        # cursor = self.db.restaurants.find()                            #search all Documents
        # cursor = self.db.restaurants.find({"borough": "Manhattan"})    #search top field
        # cursor = self.db.restaurants.find({"address.zipcode": "10075"}) #search embend object field
        # cursor = self.db.restaurants.find({"grades.grade": "C"})        #search array field
        # cursor = self.db.restaurants.find({"grades.score": {"$gt": 90}}) #最好餐厅
        # cursor = self.db.restaurants.find({"grades.score": {"$lt": 1}}) #最差餐厅 很多给了0分
        # cursor = self.db.restaurants.find({"cuisine": "Italian", "address.zipcode": "10075"}) #Logical AND
        # cursor = self.db.restaurants.find(
        #            {"$or": [{"cuisine": "Italian"}, {"address.zipcode": "10075"}]}) #Logical OR
        cursor = self.db.restaurants.find({"grades.score": {"$gt": 90}}).sort([  # 排序
            ("cuisine", pymongo.ASCENDING), ("name", pymongo.DESCENDING), ("address.zipcode", pymongo.DESCENDING)
        ])  # 排序

        # db.restaurants.
        # print "cursor length=", len(cursor)
        for document in cursor:
            print(document)

    def _update(self):
        # cursor = self.db.restaurants.find({"name": "Juni"})

        # 更新日期
        result = self.db.restaurants.update_one(
            {"name": "Juni"},  # filter
            {
                "$set": {
                    "cuisine": "American (New2)"  # $set operator 名称更新
                },
                "$currentDate": {"lastModified": True}  # $currentDate operator 日期更新操作
            }
        )

        print "[1]result.matched_count", result.matched_count
        cursor = self.db.restaurants.find({"name": "Juni"}, )
        for document in cursor:
            print(document)

        result = self.db.restaurants.update_one(
            {"restaurant_id": "41156888"},
            {"$set": {"address.street": "East 31st Street"}}
        )
        print "[2]result.matched_count", result.matched_count

    def _delete(self):
        result = self.db.restaurants.delete_many({"borough": "Manhattan"})

        print "result.deleted_count", result.deleted_count

    def _aggregate1(self):
        """
        汇聚分析
        :return:
        """
        print "_aggregate1 group by borough"
        cursor = self.db.restaurants.aggregate(
            [
                {"$group": {"_id": "$borough", "count": {"$sum": 1}}}
            ])

        for document in cursor:
            print(document)

            # print "_aggregate by $cuisine"
            # cursor = self.db.restaurants.aggregate(
            # [
            #     {"$group": {"_id": "$cuisine", "count": {"$sum": 1}}}
            # ])#.sort([("count", pymongo.ASCENDING)]) #aggregate 不支持排序
            #
            # for document in cursor:
            #     print(document)

    def _aggregate2(self):
        """
        汇聚分析, 增加 $match 删选
        :return:
        """
        print """_aggregate2 with $match borough(自治的市镇; 有议员选举权的市镇; 纽约市五个行政区之一)
                group by $address.zipcode
                The _id field contains the distinct zipcode value
              """
        cursor = self.db.restaurants.aggregate(
            [
                {"$match": {"borough": "Queens", "cuisine": "Brazilian"}},
                {"$group": {"_id": "$address.zipcode", "count": {"$sum": 1}}}  # 这里的
            ]
        )

        for document in cursor:
            print(document)

    def _create_index(self):
        """
        创建索引, 提高搜索效率
        :return:
        """
        #创建单一索引
        #print self.db.restaurants.create_index([("cuisine", pymongo.ASCENDING)])
        #创建联合索引
        print "创建联合索引 ", self.db.restaurants.create_index([
            ("cuisine", pymongo.ASCENDING),
            ("address.zipcode", pymongo.DESCENDING)
        ])


if __name__ == "__main__":
    storage_client = StorageClient()
    storage_client._save()
    # storage_client._find()
    storage_client._update()
    # storage_client._delete()
    storage_client._aggregate1()
    storage_client._aggregate2()
    storage_client._create_index()
