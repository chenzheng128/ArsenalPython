/**
 server.c的作用是从客户端读字符，然后将每个字符转换为大写并回送给客户端。
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define MAXLINE 80
#define SERV_PORT 8000

int main(void)
{
	struct sockaddr_in servaddr, cliaddr;
	socklen_t cliaddr_len;
	int listenfd, connfd;
	char buf[MAXLINE];
	char str[INET_ADDRSTRLEN];
	int i, n;

	listenfd = socket(AF_INET, SOCK_STREAM, 0);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(SERV_PORT);

    // bind()的作用是将参数sockfd和myaddr绑定在一起
	bind(listenfd, (struct sockaddr *)&servaddr, sizeof(servaddr));

    // 设置可以在所有的IP地址上监听，直到与某个客户端建立了连接时才确定下来到底用哪个IP地址
	listen(listenfd, 20);

	printf("Accepting connections ...\n");
	// 每次循环处理一个客户端连接
	while (1) {
		cliaddr_len = sizeof(cliaddr);
		// 当有客户端发起连接时，服务器调用的accept()返回并接受这个连接
		connfd = accept(listenfd,
				(struct sockaddr *)&cliaddr, &cliaddr_len);
        printf("debug: accepted a client\n");

		n = read(connfd, buf, MAXLINE);

        printf("received from at client PORT %d\n", ntohs(cliaddr.sin_port));
        // printf("received from %s\n",  inet_ntop(AF_INET, &cliaddr.sin_addr, str, sizeof(str)));
		//printf("received from %s at PORT %d\n",
		//       inet_ntop(AF_INET, &cliaddr.sin_addr, str, sizeof(str)),
		//       ntohs(cliaddr.sin_port));
		// printf("recived %s \n", buf); //TODO 如果打印这句就不能正常回显, why? 可能是读buf出错

		for (i = 0; i < n; i++)
			buf[i] = toupper(buf[i]);
		write(connfd, buf, n);  // 回显大写字符

		close(connfd);
	}
}