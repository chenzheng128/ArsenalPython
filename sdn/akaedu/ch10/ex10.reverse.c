/*
先用字符串"hello"初始化一个字符数组str（算上'\0'共6个字符）。然后用空字符串""初始化一个同样长的字符数组reverse_str，相当于所有元素用'\0'初始化。然后打印str，把str倒序存入reverse_str，再打印reverse_str。然而结果并不正确：
*/
#include <stdio.h>

int main(void)
{
	int i;
	char str[6] = "hello";
	char reverse_str[6] = "";

	printf("%s\n", str);
	for (i = 0; i < 5; i++)
		reverse_str[5-i] = str[i]; // reverse_str[5-i-1] 正确代码
	printf("%s\n", reverse_str);
	return 0;
}