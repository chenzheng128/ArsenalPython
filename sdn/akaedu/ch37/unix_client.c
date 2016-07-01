#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char *socket_path = "/tmp/sw.socket";
// char *socket_path = "\0hidden";

int main(int argc, char *argv[]) {
  struct sockaddr_un addr;
  char buf[1024];
  int fd,rc;

  if (argc > 1) socket_path=argv[1];

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

  int readcount = 0;
  while(1) {
    printf("please input your command:\t");
    fflush(stdout);
    if ((rc=read(STDIN_FILENO, buf, sizeof(buf))) <= 0) break;
    if (write(fd, buf, rc) != rc) {
      if (rc > 0) fprintf(stderr,"partial write");
      else {
        perror("write error");
        exit(-1);
      }
    }
    if ((readcount=read(fd,buf,sizeof(buf))) > 0){
          // %.*s 表示打印buf 的 readcount 长度; 如果不设定readcount长度直接打印 %s;
          // 就应该调用后面的 memset 对buf 清零,
          // 而是会因为buf中的字符不会结束在 \0 而打印出一些剩余内容否则
        printf("server echo %u bytes: \t\t%.*s", readcount, readcount, buf);
    }
    memset(&buf, 0, sizeof(buf)); //每次结束时注意清零buf, 便于字符串正常结束

  }

  return 0;
}