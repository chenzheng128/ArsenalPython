/**
使用 gdb 调试
Source: http://akaedu.github.io/book/ch10s01.html
源代码需要在当前路径下

$ gcc -g ex10.1.add.c -o ex10.1.add
$ gdb ex10.1.add

# 对应命令与简写
start
step  - s  调试子函数
print - p
finish 结束
info - i locals 查看局部变量
frame - f 1 调用 frame; f 0 当前函数, f 1 上一级函数
--------------
backtrace（或bt）	查看各级函数调用及参数
finish	连续运行到当前函数返回为止，然后停下来等待命令
frame（或f） 帧编号	选择栈帧
info（或i） locals	查看当前栈帧局部变量的值
list（或l）	列出源代码，接着上次的位置往下列，每次列10行
list 行号	列出从第几行开始的源代码
list 函数名	列出某个函数的源代码
next（或n）	执行下一行语句
print（或p）	打印表达式的值，通过表达式可以修改变量的值或者调用函数
quit（或q）	退出gdb调试环境
set var	修改变量的值
start	开始执行程序，停在main函数第一行语句前面等待命令
step（或s）	执行下一行语句，如果有函数调用则进入到函数中

*/

#include <stdio.h>

/**
add_range函数从low加到high，在main函数中首先从1加到10，把结果保存下来，然后从1加到100
*/
int add_range(int low, int high)
{
	int i, sum;
	// sum = 0; //无初始化的错误
	for (i = low; i <= high; i++)
		sum = sum + i;
	return sum;
}

int main(void)
{
	int result[100];
	int ss=1;
	result[0] = add_range(1, 10);
	result[1] = add_range(1, 100);
	printf("result[0]=%d\nresult[1]=%d\n", result[0], result[1]);
	return 0;
}
