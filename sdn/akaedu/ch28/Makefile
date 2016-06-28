
#%.o: %.c
#	$(CC) -c $<

BIN1=ex28.2.blocking

all: $(BIN1) $(BIN1).o

# 编译可执行文件到上一级./bin/目录  $@ 表示规则中的目标
$(BIN1):
	$(CC) $@.c -o ../out/$@

# 编译.o 文件, 下面这句为默认策略, 可省略
$(BIN1).o:

clean:
	rm -f *.o
	rm -f ../out/$(BIN1)