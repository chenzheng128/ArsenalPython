# linux sort 在面对特殊字符 # 表现不稳定, 修改为  sorted(); 
 # 用 objs.sort() 会报TypeError: 'NoneType' object is not iterable
#ns class_info.tcl | pawk -p 'objs=r[0].split(); print "# total otcl objects", len(objs); for x in objs: print x' | sort

ns class_info.tcl | pawk -p 'objs=r[0].split(); print "# total otcl objects", len(objs); for x in sorted(objs): print x'