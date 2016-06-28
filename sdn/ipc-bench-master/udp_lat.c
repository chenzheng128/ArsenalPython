/*
    Measure latency of IPC using tcp sockets


    Copyright (c) 2016 Erik Rigtorp <erik@rigtorp.se>

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
*/

#include <netdb.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#if defined(_POSIX_TIMERS) && (_POSIX_TIMERS > 0) &&                           \
    defined(_POSIX_MONOTONIC_CLOCK)
#define HAS_CLOCK_GETTIME_MONOTONIC
#endif

#define BUFSIZE 2048

int main(int argc, char *argv[]) {
  int size;
  char *buf;
  int64_t count, i, delta;
#ifdef HAS_CLOCK_GETTIME_MONOTONIC
  struct timespec start, stop;
#else
  // struct timeval start, stop;
#endif

  ssize_t len;
  size_t sofar;

  int yes = 1;
  int ret;
  struct sockaddr_storage their_addr;
  socklen_t addr_size;
  struct addrinfo hints;
  struct addrinfo *res;
  int new_fd;
  int recvlen;			/* # bytes received */
  int fd;				/* our socket */
  int msgcnt = 0;			/* count # of messages we received */

  struct sockaddr_in myaddr;	/* our address */
  struct sockaddr_in remaddr;	/* remote address */
  socklen_t addrlen = sizeof(remaddr);		/* length of addresses */
  char *server = "127.0.0.1";	/* change this to use a different */
  // server="192.168.57.4";  //使用外部地址发送数据
  int SERVICE_PORT = 33333;

  if (argc != 3) {
    printf("usage: udp_lat <message-size> <roundtrip-count>\n");
    return 1;
  }

  printf("debug: listen_ip=%s port=%d \n", server, SERVICE_PORT);

  size = atoi(argv[1]);
  count = atol(argv[2]);

  buf = malloc(size);
  if (buf == NULL) {
    perror("malloc");
    return 1;
  }

  //初始化本地地址
  memset((char *)&myaddr, 0, sizeof(myaddr));
  myaddr.sin_family = AF_INET;
  myaddr.sin_addr.s_addr = htonl(INADDR_ANY); //监听在ANY地址上
  myaddr.sin_port = htons(SERVICE_PORT);

  //初始化远程地址
    memset((char *) &remaddr, 0, sizeof(remaddr));
	remaddr.sin_family = AF_INET;
	remaddr.sin_port = htons(SERVICE_PORT);
	if (inet_aton(server, &remaddr.sin_addr)==0) {
		fprintf(stderr, "inet_aton() failed\n");
		exit(1);
	}

  printf("message size: %i octets\n", size);
  printf("roundtrip count: %li\n", count);

  printf("debug: before fork()\n");


  if (!fork()) { /* child */

    printf("debug: child socket() 01\n");

    if ((fd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
      perror("socket");
      return 1;
    }
    printf("debug: child socket() 02\n");

//    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
//      perror("setsockopt");
//      return 1;
//    }
    printf("debug: child set socket()\n");

    if (bind(fd, (struct sockaddr *)&myaddr, sizeof(myaddr)) < 0) {
      perror("bind");
      return 1;
    }

    printf("debug: child bind socket()\n");

    //if (listen(fd, 1) == -1) {
    //  perror("listen");
    //  return 1;
    //}

    addr_size = sizeof their_addr;

//    if ((new_fd = accept(fd, (struct sockaddr *)&their_addr, &addr_size)) ==
//        -1) {
//      perror("accept");
//      return 1;
//    }

    printf("debug: child recvfrom() \n");


    int recv_msg_count=0;
    /* now loop, receiving data and printing what we received */
	//for (;;) {
	for (i = 0; i < count; i++) {
		//printf("waiting on port %d\n", SERVICE_PORT);
		recvlen = recvfrom(fd, buf, BUFSIZE, 0, (struct sockaddr *)&remaddr, &addrlen);
		if (recvlen > 0) {
			buf[recvlen] = 0;
			// 打开这个 print 可以查看接受到的消息
			// printf("received message: \"%s\" (%d bytes)\n", buf, recvlen);
			recv_msg_count ++;
		}
		//else
		//	printf("uh oh - something went wrong!\n");
		sprintf(buf, "ack %d", msgcnt++);
		//printf("sending response \"%s\"\n", buf);
		if (sendto(fd, buf, strlen(buf), 0, (struct sockaddr *)&remaddr, addrlen) < 0)
			perror("sendto");
	}
	printf("debug: child total recv msg count=%d\n", recv_msg_count);
	printf("\n");


  } else { /* parent */

    sleep(1);

    if ((new_fd = socket(AF_INET, SOCK_DGRAM, 0)) == -1)  {
      perror("socket");
      return 1;
    }

//    if (connect(fd, res->ai_addr, res->ai_addrlen) == -1) {
//      perror("connect");
//      return 1;
//    }

#ifdef HAS_CLOCK_GETTIME_MONOTONIC
    if (clock_gettime(CLOCK_MONOTONIC, &start) == -1) {
      perror("clock_gettime");
      return 1;
    }
#else
    if (gettimeofday(&start, NULL) == -1) {
      perror("gettimeofday");
      return 1;
    }
#endif

    for (i = 0; i < count; i++) {


      //printf("parent sendto \n");

      if (sendto(new_fd, buf, strlen(buf), 0, (struct sockaddr *)&remaddr, addrlen) < 0){
        perror("write");
        return 1;
      }
      //printf("parent recvfrom\n");

      int recvlen = recvfrom(new_fd, buf, size, 0, (struct sockaddr *)&remaddr, &addrlen);

      if (recvlen > 0) {
			buf[recvlen] = 0;
			//printf("received message: \"%s\" (%d bytes)\n", buf, recvlen);
	  }

	  //printf("parent: recvlen=%d uh oh - something went wrong!\n", recvlen);
	  //else
      //  printf("parent: recvlen=%d uh oh - something went wrong!\n", recvlen);

    }

#ifdef HAS_CLOCK_GETTIME_MONOTONIC
    if (clock_gettime(CLOCK_MONOTONIC, &stop) == -1) {
      perror("clock_gettime");
      return 1;
    }
    delta = ((stop.tv_sec - start.tv_sec) * 1000000000 +
             (stop.tv_nsec - start.tv_nsec));
#else
    if (gettimeofday(&stop, NULL) == -1) {
      perror("gettimeofday");
      return 1;
    }
    delta =
        (stop.tv_sec - start.tv_sec) * 1000000000 + (stop.tv_usec - start.tv_usec) * 1000;
#endif

    printf("average latency: %li ns\n", delta / (count * 2));
  }

  return 0;
}
