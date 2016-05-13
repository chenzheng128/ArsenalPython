#-*- coding:utf-8 -*-

try: # try to use python2 module
    from urllib import urlencode
    from urllib2 import Request, urlopen, URLError
except ImportError: # otherwise, use python3 module
    from urllib.request import Request, urlopen
    from urllib.error import URLError
    from urllib.parse import urlencode

import PyBaiduYuyin as pby #原始库函数 pip install PyBaiduYuyin
#import tts_lib as pyb       #复制出来的文件

class MyTTS(pby.TTS):
    """
    重载 BaiduYuYin 原有的语音类
    """
    #def __init__(self, ):
    #    super().__init__()

    #def play_mp3(self, mp3_data):
        #super().play_mp3()
        #pass

    def save(self, text, filename, spd=5, pit=5, vol=5, per=0):
        """
        Perform TTS on the input text ``text``.

        @:param text: text to translation
        @:param spd: [optional] speed, range from 0 to 9
        @:param pit: [optional] pitch, 0-9
        @:param vol: [optional] volumn, 0-9
        @:param person: [optional] 0 for female, 1 for male
        """
        if len(text) > 1024:
            raise KeyError("Text length must less than 1024 bytes")
        url = "http://tsn.baidu.com/text2audio"

        data = {
                "tex": text,
                "lan": self.language,
                "tok": self.token,
                "ctp": 1,
                "cuid": '93489083242',
                "spd": spd,
                "pit": pit,
                "vol": vol,
                "per": per,
                }
        self.request = Request(url, data = urlencode(data))

        # check error
        try:
            response = urlopen(self.request)
        except URLError:
            raise IndexError("No internet connection available to transfer audio data")
        except:
            raise KeyError("Server wouldn't respond (invalid key or quota has been maxed out)")

        content_type = response.info().getheader('Content-Type')
        if content_type.startswith('application/json'):
            response_text = response.read().decode("utf-8")
            json_result = json.loads(response_text)
            raise LookupError("%d - %s" % (json_result['err_no'], json_result['err_msg']))
        elif content_type.startswith('audio/mp3'):
            print "write tts to file %s" % filename
            fi = open(filename,'wb')
            fi.write(response.read())
            fi.close
