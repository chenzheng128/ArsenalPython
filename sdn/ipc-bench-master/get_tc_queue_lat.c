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
  int ofds[2];
  int ifds[2];

  int size;
  char *buf;
  int64_t count, i, delta;
#ifdef HAS_CLOCK_GETTIME_MONOTONIC
  struct timespec start, stop;
#else
  struct timeval start, stop;
#endif



  if (argc < 2) {
    printf("usage: \n");
    printf("  get_tc_queue_lat <queue_id> get queue status \n");
    printf("  get_tc_queue_lat <message-size> <roundtrip-count> bench get_queue lantency \n");
    return 1;
  }

  if (argc == 2) {

    netdev_get_queue_stats(atoi(argv[1]));
    return 0;
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

  if (pipe(ofds) == -1) {
    perror("pipe");
    return 1;
  }

  if (pipe(ifds) == -1) {
    perror("pipe");
    return 1;
  }

  if (!fork()) { /* child */
    for (i = 0; i < count; i++) {

      if (read(ifds[0], buf, size) != size) {
        perror("read");
        return 1;
      }

      if (write(ofds[1], buf, size) != size) {
        perror("write");
        return 1;
      }
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

    for (i = 0; i < count; i++) {

      if (write(ifds[1], buf, size) != size) {
        perror("write");
        return 1;
      }

      if (read(ofds[0], buf, size) != size) {
        perror("read");
        return 1;
      }
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



int
netdev_get_queue_stats(unsigned int queue_id)
{
    // const struct netdev_class *class = netdev->netdev_class;
    //ZHL
    int finalpack = 0;
    char search[10]="backlog";
    // char *command = "tc -s class ls dev s2-eth2 parent 1:fffe classid 1:3";   //this is the command that we used to test
    // char *netname = netdev_get_name(netdev);  //netdevice's name
    char *netname = "s1-eth3";  //netdevice's name
    char commone[80] = "tc -s class ls dev ";
    char *commtwo = " parent 1:fffe classid 1:";
    char commthree[3] = "";


    strcat(commone,netname);
    strcat(commone,commtwo);
    sprintf(commthree,"%d",queue_id);
    strcat(commone,commthree); //  now we construct the query command successfully.
    // VLOG_INFO(commone);   // test is end ,now we do not need to output the command line
    printf("debug: 01 %s\n", commone);

    FILE *pp = popen(commone, "r");   // now we executed the query command.
    if (!pp) {
        return -1;
    }

    char tmp[1024];

    printf("debug: 02 %s\n", commone);

    while (fgets(tmp, sizeof(tmp), pp) != NULL) {
        if (tmp[strlen(tmp) - 1] == '\n') {
            tmp[strlen(tmp) - 1] = '\0';
        }
        char *myp;
        myp = strstr(tmp,search);
        printf("debug: 03-1 %s\n", myp);
        if(myp){
            char delims[] = " ";
            char *result = NULL;
            printf("debug: 03-2 myp='%s' delim='%s'\n", myp, delims);
            /*
            TODO strok Segmenation falut in here 
            */
            result = strtok( myp, delims );
            printf("debug: 03-3 %s\n", result);
            while( result != NULL ) {
                if(strstr(result,"p")){
                    finalpack = atoi(result);  //get the left packets data and transfer it to int type.
		    break;
                }
                result = strtok( NULL, delims );
           }
        }

    }
    pclose(pp);

    printf("%s\n", commone);
    return 0;

    printf("finalpack %d", finalpack);
    //zZHL
    return finalpack;
}
