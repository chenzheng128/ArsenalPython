/* server.c */
#include <stdio.h>
#include <string.h>
#include <netinet/in.h>
//#include "wrap.h"

#define MAXLINE 80
#define SERV_PORT 8000

int main(void)
{
	struct sockaddr_in servaddr, cliaddr;
	socklen_t cliaddr_len;
	int sockfd;
	char buf[MAXLINE];
	char str[INET_ADDRSTRLEN];
	int i, n;

	//if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ){
	if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
	    perror("cannot create socket\n");
		return 0;
	}

	// bzero(&servaddr, sizeof(servaddr));
	memset((char *)&servaddr, 0, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(SERV_PORT);

	if (bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) ){
        perror("bind failed");
		return 0;
	}

	printf("Accepting connections ...\n");
	while (1) {
		cliaddr_len = sizeof(cliaddr);
		// TODO 总是收到数据后崩溃 Segmentation fault (core dumped)  这里
		n = recvfrom(sockfd, buf, MAXLINE, 0, (struct sockaddr *)&cliaddr, &cliaddr_len);
		if (n == -1)
			perr_exit("recvfrom error");
        printf("received from %s at PORT");

        /*
        printf("received from %s at PORT %d\n",
        inet_ntop(AF_INET, &cliaddr.sin_addr, str, sizeof(str)),
        ntohs(cliaddr.sin_port));

		for (i = 0; i < n; i++)
			buf[i] = toupper(buf[i]);
		n = sendto(sockfd, buf, n, 0, (struct sockaddr *)&cliaddr, sizeof(cliaddr));
		if (n == -1)
			perr_exit("sendto error");
		*/
	}
}