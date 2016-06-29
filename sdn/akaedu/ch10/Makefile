# -g 运行调试
# CFLAGS = -g -Wall -O3
# CFLAGS = -g -O3 -w # disable warning
CFLAGS = -g  # 如果用-O3编译, gdb将不支持 set val 操作

#%.o: %.c
#	$(CC) -c $<

all: ex10.1.add ex10.2.break ex10.reverse \
    ex10.3.watch \
    ex10.4.segm_fault ex10.5.segm_fault2


# 编译可执行文件到上一级./bin/目录  $@ 表示规则中的目标
# ex25.2.strok:
# 	$(CC) $@.c -o ../out/$@

# 编译.o 文件, 下面这句为默认策略, 可省略
# ex25.2.strok.o:

clean:
	rm -f *.o
	rm -f ex10.1.add
	rm -f ex10.2.break
	rm -f ex10.reverse
	rm -f ex10.3.watch
	rm -f ex10.4.segm_fault
	rm -f ex10.5.segm_fault2