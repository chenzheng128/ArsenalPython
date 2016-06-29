#include <stdio.h>
#include <string.h>

int main(void)
{
	char buf[20] = "hello world";
	printf (" %s strlen()=%d\n", buf, strlen(buf)); //字符串长度

    // memcpy的两个参数src和dest所指的内存区间如果重叠则无法保证正确拷贝，
        // 而memmove却可以正确拷贝
	memmove(buf + 1, buf, 13);

	printf("%s\n", buf);

	char dst[10] = "foo";
    char src[10] = "bar";
    strcat(dst, src);
    printf("strcat(): %s %s\n", dst, src); //字符串连接


    printf("strcmp(%s, %s): %d \n", dst, src, strcmp(dst, src)); //字符串比较
    printf("strcmp(%s, %s): %d \n", src, src, strcmp(src, src)); //字符串比较

    char *p = NULL;
    p = strstr(dst, src);
    printf("strstr() found:  %s\n", p); //字符串搜索
//    //    printf("strstr(%s, %s): %s \n", dst, src, p); //字符串搜索

    char haystack[20] = "TutorialsPoint";
    char needle[10] = "Point";
    char *ret;

    ret = strstr(haystack, needle); //字符串搜索

    printf("The substring is: %s\n", ret);
	return 0;
}

