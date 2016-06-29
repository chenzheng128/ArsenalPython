/**

个程序的作用是：首先从键盘读入一串数字存到字符数组input中，然后转换成整型存到sum中，然后打印出来，一直这样循环下去。

make && gdb ex10.2.break

display 命令使得每次停下来的时候都显示当前sum的值
undisplay 命令可以取消跟踪显示
break 命令的参数也可以是函数名，表示在某个函数开头设断点

(gdb) break 19 if sum != 0 # 条件断点

-----
命令	描述
break（或b） 行号	在某一行设置断点
break 函数名	在某个函数开头设置断点
break ... if ...	设置条件断点
continue（或c）	从当前位置开始连续运行程序
delete breakpoints 断点号	删除断点
display 变量名	跟踪查看某个变量，每次停下来都显示它的值
disable breakpoints 断点号	禁用断点
enable 断点号	启用断点
info（或i） breakpoints	查看当前设置了哪些断点
run（或r）	从头开始连续运行程序
undisplay 跟踪显示号	取消跟踪显示


*/
#include <stdio.h>

int main(void)
{
	int sum = 0, i = 0;
	char input[5];

	while (1) {
	    // sum = 0; 缺少的赋值语句
		scanf("%s", input);
		for (i = 0; input[i] != '\0'; i++)
			sum = sum*10 + input[i] - '0';
		printf("input=%d\n", sum);
	}
	return 0;
}