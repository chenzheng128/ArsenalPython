#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <sys/socket.h>
#include <sys/un.h>

/*
 创建并绑定一个一个unix文件套接字

 ls /tmp/sdn; # 查看创建的套接字
 rm /tmp/sdn/aka*.socket; #删除套接字
*/
int main(void)
{
	int fd, size;
	struct sockaddr_un un;

	memset(&un, 0, sizeof(un));
	un.sun_family = AF_UNIX;
	strcpy(un.sun_path, "/tmp/sdn/aka_foo.socket");
	if ((fd = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) {
		perror("socket error");
		exit(1);
	}
	// offsetof(struct sockaddr_un, sun_path)就是取sockaddr_un结构体的sun_path成员在结构体中的偏移，
	// 也就是从结构体的第几个字节开始是sun_path成员
	size = offsetof(struct sockaddr_un, sun_path) + strlen(un.sun_path);
	if (bind(fd, (struct sockaddr *)&un, size) < 0) {
		perror("bind error");
		exit(1);
	}
	printf("UNIX domain socket bound\n");
	exit(0);
}