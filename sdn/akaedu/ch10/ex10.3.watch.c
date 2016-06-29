/**

平台相关, 在linux没出现文档的效果.
Source: http://akaedu.github.io/book/ch10s03.html

表 10.3. gdb基本命令3

命令	描述
watch	设置观察点
info（或i） watchpoints	查看当前设置了哪些观察点
x	从某个位置开始打印存储单元的内容，全部当成字节来看，而不区分哪个字节属于哪个变量
*/

#include <stdio.h>

int main(void)
{
	int sum = 0, i = 0;
	char input[5];

	while (1) {
		sum = 0;
		scanf("%s", input);
		for (i = 0; input[i] != '\0'; i++)
			sum = sum*10 + input[i] - '0';
		printf("input=%d\n", sum);
	}
	return 0;
}