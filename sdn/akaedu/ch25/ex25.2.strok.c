#include <stdio.h>
#include <string.h>

int main(void)
{
	char str[] = "root:x::0:root:/root:/bin/bash:";
	char *token;

	token = strtok(str, ":");
	printf("%s\n", token);
	while ( (token = strtok(NULL, ":")) != NULL)
		printf("%s\n", token);

	return 0;
}
