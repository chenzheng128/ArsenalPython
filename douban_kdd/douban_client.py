#coding: utf-8
import requests
#import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings() # 取消警告

import logging
log = logging.getLogger(__name__)

class DoubanClient(object):
    def __init__(self):
        self.api_entry = "https://api.douban.com/v2"
        self.access_token = ""
    """
    6大排行版, 后2个没权限
    """
    def movie_in_theaters(self):
        return self._get_list_all("/movie/in_theaters", params={"count": "100"})
    def movie_coming_soon(self):
        return self._get_list_all("/movie/coming_soon", params={"count": "100"})
    def movie_top250(self):
        return self._get_list_all("/movie/top250", params={"count": "250"})
    def movie_us_box(self):
        return self._get_list_all("/movie/us_box", params={"count": "100"})
    def movie_weekly(self):
        return self._get_list_all("/movie/weekly", params={"count": "100"})
    def movie_new_movies(self):
        return self._get_list_all("/movie/new_movies", params={"count": "100"})

    def movie_subject(self, id):
        """
        电影条目信息( 详细信息, 评论 等)
        :return:
        """
        return self._get("/movie/subject/%s" % id )#, params={"id": id})

    def _get_list_all(self, path, params=None):
        """
        TODO 增加一些判断处理, 如果返回的  subjects 数量< total, 增加新的start请求
        获取所有数据
        :param path:
        :param params:
        :return:
        """
        if not params:
            params = {}
        params['access_token'] = self.access_token
        rsp = requests.get(self.api_entry + path, params=params,
                           verify=False)
        content, error = self._process_response(rsp)
        if content == None:
            print error, rsp.url
            log.warn("%s"  % (error))
        return content, error

    def _get(self, path, params=None):
        """
        基本的get方法
        :param path:
        :param params:
        :return:
        """
        if not params:
            params = {}
        params['access_token'] = self.access_token
        rsp = requests.get(self.api_entry + path, params=params,
                           verify=False)
        return self._process_response(rsp)

    def _process_response(self, rsp):
        """
        基本的响应处理方法
        :param rsp:
        :return:
        """

        if rsp.status_code != 200 and rsp.status_code != 403:
            return None, APIError(rsp.status_code, 'http error')
        try:
            content = rsp.json()
        except:
            return None, APIError(99999, 'invalid rsp (not json) ')

        if rsp.status_code == 403:
            error = APIError(rsp.status_code, rsp.content, "0")
            if  'code' in content:
                error.code = content['code']
            return None, error
        return content, None

class APIError(object):
    def __init__(self, status, content, code=-1):
        self.status = status
        self.content = content
        self.code = code

    def __repr__(self):
        return self.__unicode__()
    def __unicode__(self):
        return ("APIError status:%s code:%s content:%s " % (self.status, self.code, self.content))