#include <stdio.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdlib.h>

char *socket_path = "/tmp/bench.socket";
// char *socket_path = "\0hidden";
struct sockaddr_un addr;
int fd;

int main(int argc, char *argv[]) {


  int sv1; /* the pair of socket descriptors */
  int expect_recv_size = 0;
  int expect_send_size = 0;
  char buf[1024];
  int64_t count, i, delta;
#ifdef HAS_CLOCK_GETTIME_MONOTONIC
  struct timespec start, stop;
#else
  struct timeval start, stop;
#endif

  if (argc != 3) {
    printf("usage: unix_lat <expect_recv_size> <expect_send_size>\n");
    return 1;
  }

  expect_recv_size = atoi(argv[1]);
  expect_send_size = atol(argv[2]);

  //buf = malloc(size);
  if (buf == NULL) {
    perror("malloc");
    return 1;
  }

  printf("message expect_recv_size: %i octets\n", expect_recv_size);
  printf("message expect_send_size: %i octets\n", expect_send_size);
  printf("roundtrip count: end less \n");


  addr.sun_family = AF_UNIX;
  if (*socket_path == '\0') {
    *addr.sun_path = '\0';
    strncpy(addr.sun_path+1, socket_path+1, sizeof(addr.sun_path)-2);
  } else {
    strncpy(addr.sun_path, socket_path, sizeof(addr.sun_path)-1);
  }

  unlink(socket_path);

  if ( (fd = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
    perror("socket error");
    exit(-1);
  }
  // 如果绑定不上, 应检查该目录权限问题
  printf ("debug: binding on socket_path: %s\n", socket_path);
  if (bind(fd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
    perror("bind error");
    exit(-1);
  }

  if (listen(fd, 5) == -1) {
    perror("listen error");
    exit(-1);
  }




  int readcount=0;
  int writecount=0;

  while(1) {
    if ( (sv1 = accept(fd, NULL, NULL)) == -1) {
      perror("accept error");
    }
    while(1){
        if ((readcount=read(sv1, buf, expect_recv_size)) != expect_recv_size) {
            printf ("partial read count %d\n" , readcount);
            perror("read");
            // return 1;
        }

        // printf("read client %u bytes: %.*s\n", size, 10, buf);

        if ((writecount=write(sv1, buf, expect_send_size)) != expect_send_size) {
            printf ("partial write count %d\n" , writecount);
            perror("write");
            // return 1;
        }
        // printf ("write somthing\n");
    }
  }


  return 0;
}