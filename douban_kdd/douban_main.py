# coding: utf-8

"""
filename:
每天处理的任务, 获取榜单信息
"""
import time
from datetime import datetime
from douban_client import DoubanClient
from douban_mongo import StorageClient
import logging

log = logging.getLogger(__name__)

BREAK_INTERVEL_MINUTES = 6 * 60  # after how many minutes
BREAK_INTERVEL_SECONDS = BREAK_INTERVEL_MINUTES * 60


# BREAK_INTERVEL_SECONDS = 5 #for debugging


def task_movie_list():
    """
    获取列表任务 请求*4
    :return:
    """
    now = datetime.now()
    # now=datetime.now() - START_TIME
    # run_seconds=BREAK_SECOND-now.seconds

    # 可以正常访问的4个接口
    content, error = douban_client.movie_in_theaters()
    mongo_client.save_movie_in_theaters(content)
    content, error = douban_client.movie_coming_soon()
    mongo_client.save_movie_coming_soon(content)
    content, error = douban_client.movie_us_box()
    mongo_client.save_movie_us_box(content)

    # content, error = douban_client.movie_top250()
    # mongo_client.save_movie_top250(content)

    # 缺少api权限的接口 {"msg":"need_permission","code":1000,"request":"GET \/v2\/movie\/weekly"}
    # content, error = douban_client.movie_weekly()
    # mongo_client.save_movie_weekly(content)
    # content, error = douban_client.movie_new_movies()
    # mongo_client.save_movie_new_movies(content)


    log.warn("got date success %s %s " % (now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%s")))


def task_movie_subject_recent():
    """
    获取 最近电影 详细信息 任务 请求*100
    :return:
    """
    now = datetime.now()
    # now=datetime.now() - START_TIME
    # run_seconds=BREAK_SECOND-now.seconds

    ids = list(mongo_client.get_movies_subject_ids_recent())  # 从 mongodb collects 中获取不重复的id列表, 便于下一次抓取
    log.warn("length(ids) %s", len(ids))
    # id = ids[0]
    for id in ids:
        if mongo_client.subject_existed("subject_recent", id): # 如果已经有此条数据， 则跳过抓取, 优化抓取效率
            continue
        content, error = douban_client.movie_subject(id)
        if content != None:
            mongo_client.save_movie_subject(id, content)  # 抓取这些电影信息并保存
            # mongo_client.collect_movie_subject(id, content)
        else:
            print content, error
            # break
    log.warn("got date success %s %s " % (now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%s")))


if __name__ == "__main__":
    level = logging.WARNING
    level = logging.DEBUG
    logging.basicConfig(format='%(name)s \t\t%(levelname)-8s %(filename)8s %(funcName)8s() [%(message)-60s] %(module)s',
                        level=level)
    START_TIME = datetime.now()
    douban_client = DoubanClient()
    mongo_client = StorageClient()
    while True:
        content, error = douban_client.movie_in_theaters()  # 测试抓取,
        if content == None and error.code == 112:
            print "我们抓取的太快了, 休息一下 ..."
            time.sleep(BREAK_INTERVEL_SECONDS)  # 如果抓取太快, 等候下一轮抓取

        break
        print ("抓取最近电影列表, 保存至 mongodb ...")
        # task_movie_list()
        print ("提取不重复 id，抓取电影详细信息至 mongodb ...")
        task_movie_subject_recent()
        time.sleep(BREAK_INTERVEL_SECONDS)
        
        #break  # debug
