#-*- coding:utf-8 -*-

import wave #
import json #
import urllib2,pycurl

def get_token():
	apiKey = 'pBcpTAFCEj1yeSDFUjpvbwCz'
	secretKey = 'oZzcl3EOTK6Wl6bKVOG5CdWTHzw3BjuU'
	getTokenURL =  "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret="+secretKey
	res = urllib2.urlopen(getTokenURL)
	json_data = res.read()
	return json.loads(json_data)['access_token']

def dump_res(buf):
	print buf

def use_cloud(token):
	fp = wave.open('test.wav','rb')
	nf = fp.getnframes()
	f_len = nf * 2
	audio_data = fp.readframes(nf)
	cuid = "6061300"
	srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
	http_header = [
		'Content-Type:audio/wav;rate=16000'
		'Content-Length:%d'%f_len
	]
    # file rate and file length

	c = pycurl.Curl()
	c.setopt(pycurl.URL,str(srv_url))
	c.setopt(c.HTTPHEADER,http_header)
	c.setopt(c.POST,1)
	c.setopt(c.CONNECTTIMEOUT,60)
	c.setopt(c.TIMEOUT,60)
	c.setopt(c.WRITEFUNCTION,dump_res)
	c.setopt(c.POSTFIELDS,audio_data)
	c.setopt(c.POSTFIELDSIZE,f_len)
	c.perform()

if __name__== "__main__":
	token=get_token()
	print token
	use_cloud(token)
	print 'finish'
