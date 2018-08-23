#coding:utf-8
#CalThreeKingdomsV1.py
# 下载文本地址 https://www.icourse163.org/learn/BIT-268001?tid=1002788003#/learn/content?type=detail&id=1004072178&cid=1005006157
# 下载地址 https://www.icourse163.org/course/attachment.htm?fileName=%E5%AE%9E%E4%BE%8B10-%E6%96%87%E6%9C%AC%E8%AF%8D%E9%A2%91%E7%BB%9F%E8%AE%A1%E6%BA%90%E4%BB%A3%E7%A0%81.zip&nosKey=3EB5816FF36E20A17232A1CE826DAA79-1523925499203
import jieba
txt = open("threekingdoms.txt", "r", encoding='utf-8').read()
words  = jieba.lcut(txt)
counts = {}
for word in words:
    if len(word) == 1:
        continue
    else:
        counts[word] = counts.get(word,0) + 1
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True) 
for i in range(15):
    word, count = items[i]
    print ("{0:<10}{1:>5}".format(word, count))
