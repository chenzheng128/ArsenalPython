#-*- coding:utf-8 -*-

from TTS.tts_lib import MyTTS

from config import *        #YOUR_APP_KEY / YOUR_SECRET_KEY 秘钥


#  #使用复制出的 ttslib文件进行替换
tts = MyTTS(app_key=YOUR_APP_KEY, secret_key=YOUR_SECRET_KEY)
tts.say("你好")
tts.save("这是一个百度语音例子", "tmp.mp3")
