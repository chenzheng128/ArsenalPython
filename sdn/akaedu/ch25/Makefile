
#%.o: %.c
#	$(CC) -c $<

all: ex25.2.strok \
	ex25.1.strfun

# 编译可执行文件到上一级./bin/目录  $@ 表示规则中的目标
# ex25.2.strok:
#	$(CC) $@.c -o ../out/$@

# 编译.o 文件, 下面这句为默认策略, 可省略
# ex25.2.strok.o:

clean:
	rm -f *.o
	rm -f ex25.2.strok
	rm -f ex25.1.strfun