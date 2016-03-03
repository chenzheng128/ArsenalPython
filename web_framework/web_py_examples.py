#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

class index:
    def GET(self):
    	#STEP1 simple hello
        #return "Hello, world!"

        #STEP2 using template
        #name = "Zheng Chen"
        #name = ""
        #return render.index(name)

        #STEP3
		i = web.input(name1=None)
		return render.index(i.name1) #为什么该成name1了，在页面中仍然还能识别呢？



urls = ('/', 'index')
app = web.application(urls, globals())
render = web.template.render('web_py_templates/')


if __name__ == "__main__":
	app.run()
