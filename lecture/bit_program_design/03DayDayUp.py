#coding:utf-8

#DayDayUpQ1.py
print("\n=== 版本V1 ===")
dayup = pow(1.001, 365)
daydown = pow(0.999, 365)
print("向上：{:.2f}，向下：{:.2f}".format(dayup, daydown))

#DayDayUpQ2.py
print("\n=== 版本V2 ===")
dayfactor = 0.001
dayup = pow(1+dayfactor, 365)
daydown = pow(1-dayfactor, 365)
print("向上：{:.2f}，向下：{:.2f}".format(dayup, daydown))

#DayDayUpQ3.py
print("\n=== 版本V3 ===")
dayup = 1.0
dayfactor = 0.01
for i in range(365):
   if i % 7 in [6,0]:
       dayup = dayup*(1-dayfactor)
   else:
       dayup = dayup*(1+dayfactor)
print("工作日的力量：{:.2f} ".format(dayup))

#DayDayUpQ4.py
print("\n=== 版本V4 ===")
def dayUP(df):
    dayup = 1
    for i in range(365):
       if i % 7 in [6,0]:
           dayup = dayup*(1 - 0.01)
       else:
           dayup = dayup*(1 + df)
    return dayup
dayfactor = 0.01
while dayUP(dayfactor) < 37.78:  # TODO 37.78 是什么？
    dayfactor += 0.001

# Python format 格式化函数 http://www.runoob.com/python/att-string-format.html
print("工作日的努力参数是：{:.3f} ".format(dayfactor))