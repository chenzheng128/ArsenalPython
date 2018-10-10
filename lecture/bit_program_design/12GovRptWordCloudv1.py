#GovRptWordCloudv1.py
import jieba
import wordcloud
import os

src_file="threekingdoms.txt"
src_file="12test.txt"

f = open(src_file, "r", encoding="utf-8")
 
t = f.read()
f.close()
ls = jieba.lcut(t)
 
txt = " ".join(ls)
w = wordcloud.WordCloud( \
    width = 1000, height = 700,\
    background_color = "white",
    # 设置正确的字体目录，避免 “OSError: cannot open resource” 错误
    # Windows
    # font_path = "msyh.ttc"    
    # Mac   
    font_path = "/Library/Fonts/Songti.ttc"    
    )
w.generate(txt)
w.to_file("12grwordcloud.png")
os.system("open 12grwordcloud.png")
