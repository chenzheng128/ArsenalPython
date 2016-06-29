#include <stdio.h>

int main(void)
{
	int sum = 0, i = 0;
	char input[5];

	scanf("%s", input);
	for (i = 0; input[i] != '\0'; i++) {
		if (input[i] < '0' || input[i] > '9') {
			printf("Invalid input!\n");
			sum = -1;
			break;
		}
		sum = sum*10 + input[i] - '0';
	}
	printf("input=%d\n", sum);
	return 0;
} // scanf 输入超长时, 错误发生地址

/**
，如果某个函数的局部变量发生访问越界，有可能并不立即产生段错误，而是在函数返回时产生段错误。
*/