/*
    Measure latency of IPC using unix domain sockets


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

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#if defined(_POSIX_TIMERS) && (_POSIX_TIMERS > 0) &&                           \
    defined(_POSIX_MONOTONIC_CLOCK)
#define HAS_CLOCK_GETTIME_MONOTONIC
#endif

int main(int argc, char *argv[]) {
  int sv[2]; /* the pair of socket descriptors */
  int size;
  char *buf;
  int64_t count, i, delta;
#ifdef HAS_CLOCK_GETTIME_MONOTONIC
  struct timespec start, stop;
#else
  struct timeval start, stop;
#endif

  if (argc != 3) {
    printf("usage: unix_lat <message-size> <roundtrip-count>\n");
    return 1;
  }

  size = atoi(argv[1]);
  count = atol(argv[2]);

  buf = malloc(size);
  if (buf == NULL) {
    perror("malloc");
    return 1;
  }

  printf("message size: %i octets\n", size);
  printf("roundtrip count: %li\n", count);

  if (socketpair(AF_UNIX, SOCK_STREAM, 0, sv) == -1) {
    perror("socketpair");
    return 1;
  }

  if (!fork()) { /* child */

    // printf ("debug: child loop one...");

    for (i = 0; i < count; i++) {
    //   if (read(sv[1], buf, size) != size) {
    //     perror("read");
    //     return 1;
    //   }
      //
    //   if (write(sv[1], buf, size) != size) {
    //     perror("write");
    //     return 1;
    //   }
        // run_sys();
        //get_popen();
    }
  } else { /* parent */

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

    //printf ("parent loop two ...");

    for (i = 0; i < count; i++) {

    //   if (write(sv[0], buf, size) != size) {
    //     perror("write");
    //     return 1;
    //   }
      //
    //   if (read(sv[0], buf, size) != size) {
    //     perror("read");
    //     return 1;
    //   }

        // 休息 1 ms, //usleep 的时间不准确, usleep(1) 约 32us
        usleep(1000);
        run_sys();
        // run_cmd();
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


void run_sys(){
    // 会打印输出, 暂不适合使用
    // system("ls >/dev/null 2>&1");  // 1 285 494 ns
    // system("pwd >/dev/null 2>&1"); // 241,402 ns
    // sudo 开销会大一些
    // system("sudo ifconfig eth0 txqueuelen 99 "); //2,900,697 ns
    //system("sudo tc class show dev eth0 >/dev/null 2>&1"); //3,044,673 ns

    /* 初始化 qdisc 便于测试 tc class change 一下命令
    sudo -s
    #删除
    tc qdisc del dev eth0 root
    #初始化
    tc qdisc add dev eth0 root handle 1: htb default 30
    tc class add dev eth0 parent 1: classid 1:1 htb rate 6mbit burst 15k
    tc class add dev eth0 parent 1:1 classid 1:10 htb rate 5mbit burst 15k
    tc class add dev eth0 parent 1:1 classid 1:20 htb rate 3mbit ceil 6mbit burst 15k
    tc class add dev eth0 parent 1:1 classid 1:30 htb rate 1kbit ceil 6mbit burst 15k
    */
    // change
    //system("tc class change dev s2-eth2 parent 1:fffe classid 1:2 htb rate 4mbit burst 15k"); // average latency: 0.7ms, 735us, 735,628 ns
    //
    system("tc -s -d class show dev s2-eth1 >/dev/null 2>&1");

}

void run_cmd() {
    FILE *pf;
    char command[20];
    char data[512];

    // Execute a process listing
    sprintf(command, "pwd"); // 34us, 33582 ns

    // sprintf(command, "ifconfig eth0 txqueuelen 100"); // always crashed
    // sprintf(command, "tc class show dev eth0"); //
    // usleep(1000);

    // Setup our pipe for reading and execute our command.
    pf = popen(command,"r");

    // Error handling

    // Get the data from the process execution
    fgets(data, 512 , pf);

    // the data is now in 'data'

    if (pclose(pf) != 0)
        fprintf(stderr," Error: Failed to close command stream \n");

    return;
}
