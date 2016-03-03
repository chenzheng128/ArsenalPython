# -*- coding: utf-8 -*-

from dingding.enterprise import DingDingApi
from config import DingTalkConfig

def getDepts(ddApi):
    """
    :type ddApi: DingDingApi
    :rtype:
    """
    depts, apiErr = ddApi.departments()
    print type(depts), depts
    #for key, value in depts.iteritems():
    #    print key, value
    if len(depts)>0: depts = depts["department"]
    for dept in depts:
        print dept

##初始化
ddApi = DingDingApi(DingTalkConfig.CorpID, DingTalkConfig.CorpSecret)

##获取token
print ddApi.get_access_token()

#获取部门
getDepts(ddApi)
