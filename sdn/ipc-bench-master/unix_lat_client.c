#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char *socket_path = "/var/sdn/bench.socket";
// char *socket_path = "\0hidden";
struct sockaddr_un addr;


int main(int argc, char *argv[]) {
  int fd; /* the pair of socket descriptors */
  int expect_recv_size = 0;
  int expect_send_size = 0;
  char buf[1024];
  int64_t count, i, delta;
#ifdef HAS_CLOCK_GETTIME_MONOTONIC
  struct timespec start, stop;
#else
  struct timeval start, stop;
#endif

  if (argc != 4) {
    printf("usage: ./unix_lat_client \"command\" <expect_recv_size> <roundtrip-count>\n");
    // printf("usage: unix_lat 22 <roundtrip-count>\n");
    return 1;
  }

  expect_send_size = strlen(argv[1])+1;
  expect_recv_size = atoi(argv[2]);
  count = atol(argv[3]);

  // buf = malloc(size);
  // memset(&buf, 'o', sizeof(buf)); buf[size-1]=0;
  if (buf == NULL) {
    perror("malloc");
    return 1;
  }

  printf("message content: %s \n", argv[1]);
  printf("message size: %i octets\n", expect_send_size);
  printf("roundtrip count: %li\n", count);


  if ( (fd = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
    perror("socket error");
    exit(-1);
  }

  memset(&addr, 0, sizeof(addr));
  addr.sun_family = AF_UNIX;
  if (*socket_path == '\0') {
    *addr.sun_path = '\0';
    strncpy(addr.sun_path+1, socket_path+1, sizeof(addr.sun_path)-2);
  } else {
    strncpy(addr.sun_path, socket_path, sizeof(addr.sun_path)-1);
  }

  printf ("debug: connet on socket_path: %s\n", socket_path);
  if (connect(fd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
    perror("connect error");
    exit(-1);
  }


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

    int readcount=0;
    int writecount=0;

    for (i = 0; i < count; i++) {
      // printf("command argv[1]=%s\n", argv[1]);
      if ((writecount=write(fd, argv[1], expect_send_size)) != expect_send_size) {
        printf ("partial writecount %d\n" , writecount);
        perror("write");
        //return 1;
      }
      //printf ("write somthing\n");

      if ((readcount=read(fd, buf, expect_recv_size)) != expect_recv_size) {
        //printf ("partial readcount=%d \n" , readcount);
        printf ("partial readcount=%d: %.*s\n" , readcount, readcount, buf);

        perror("read");
        //return 1;
      }
      //printf ("read somthing\n");
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


  return 0;
}