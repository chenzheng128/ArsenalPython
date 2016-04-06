# -*- coding:utf-8 -*-
import logging
import json
from datetime import datetime

"""
https://docs.python.org/2/library/json.html
"""

log = logging.getLogger(__name__)


def dumps():
    log.info("=== dump start ===")
    json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    print(json.dumps("\"foo\bar"))
    print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))

    print "-- default print "
    print "  ", json.dumps([1, 2, 3, {'4': 5, '6': 7}])  # , separators=(',',':'))
    print "-- compat print"
    print "  ", json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))  # 压缩了空格 ' ,' -> ','

    print "-- pretty print"
    print "  ", json.dumps({'4': 5, '6': 7},  # sort_keys=True,
                           indent=4,  # separators=(',', ': ')
                           )

    pass


def load():
    log.info("=== load start ===")
    # >>> import json
    # >>>
    print json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
    # [u'foo', {u'bar': [u'baz', None, 1.0, 2]}]
    # >>>
    print json.loads('"\\"foo\\bar"')
    # u'"foo\x08ar'
    # >>>
    from StringIO import StringIO
    io = StringIO('["streaming API"]')
    print "-- load 中文"
    print json.load(io)
    # [u'streaming API']

    complex_str = StringIO(u""" {
  "records": "5270",
  "total": "264",
  "page": "1",
  "items": [1, 5, 6, 7, 8],
  "cn" : "中文",
  "主键" : "键值"
       }""")
    myjson = json.load(complex_str)
    print myjson
    if isinstance(myjson, dict):
        print myjson["cn"]

    return myjson
    #pass


"""
$ echo '{"json":"obj"}' | python -mjson.tool
{
    "json": "obj"
}
$ echo '{1.2:3.4}' | python -mjson.tool
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

curl 获取JSON
curl --cookie "JSESSIONID=xxxxxxx" -d request.json -o output.json http://localhost/xxx_ajax.jsp

python 格式化
cat output.json | python -mjson.tool
"""


def to_bean():
    log.info("=== to_bean() start ===")
    # >>> import json
    def as_complex(dct):
        if '__complex__' in dct:
            return complex(dct['real'], dct['imag'])
        return dct

    print json.loads('{"__complex__": true, "real": 1, "imag": 2}',
                     object_hook=as_complex )  #使用 oject_hook 重建对象
    # (1+2j)
    import decimal
    print json.loads('1.1', parse_float=decimal.Decimal) #使用 parse_float 处理浮点数
    # Decimal('1.1')

def insert(data):
    """
    插入数据
    :param data:
    :return:
    """
    #pass
    data["timestamp"] = datetime.now().strftime("%s")
    data["timestr"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.info("插入timestr到json对象中 %s" % data)

def main():
    log.info("=== main start ===")
    dumps()
    myjson = load()
    to_bean()
    log.info( "获取到json对象 \t\t %s" % myjson)
    insert(myjson)


if __name__ == "__main__":
    logging.basicConfig(format='%(name)s %(levelname)-8s %(filename)8s %(funcName)8s() [%(message)-60s] %(module)s',
                        level=logging.DEBUG)
    main()
