# Source: https://akaedu.github.io/book/ch22s01.html
# 注意: Makefile 必须使用Tab作为分隔, 空格不行
#
# make -p # 打印隐含规则
#
# 特殊变量 https://akaedu.github.io/book/ch22s03.html
# $@，表示规则中的目标。
# $<，表示规则中的第一个条件。
# $?，表示规则中所有比目标新的条件，组成一个列表，以空格分隔。
# $^，表示规则中的所有条件，组成一个列表，以空格分隔。
#
# 例如前面写过的这条规则：
#
# main: main.o stack.o maze.o
# 	gcc main.o stack.o maze.o -o main
# 可以改写成：
# $@ main
#
# main: main.o stack.o maze.o
# 	gcc $^ -o $@

foo = $(bar)
bar = "start building"

# 代码目录
CODE_DIR = \
    ch25 \
	ch28

.PHONY: project_code


project_code:
	# 编译各个目录代码
	for number in $(CODE_DIR) ; do \
		$(MAKE) -C $$number ; \
	done
	# 编译完成 ...

clean:
	@echo "cleanning project"
	-rm -f *.o
	-rm -f bin/*
	# 编译各个目录代码
	for number in $(CODE_DIR) ; do \
		$(MAKE) -C $$number clean; \
	done
	# 清除完成 ...

forloop:
	# 打印 for-loop 测试
	for number in 1 2 3 4 ; do \
		echo $$number ; \
	done


