#include <stdio.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdlib.h>

char *socket_path = "/tmp/sw.socket";
// char *socket_path = "\0hidden";


int main(int argc, char *argv[]) {
  struct sockaddr_un addr;
  char buf[100];            //单行缓存
  char buf_mutiline[500];   //多行缓存
  int fd,client_fd,readcount;

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


  unlink(socket_path);

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

  while (1) {
    if ( (client_fd = accept(fd, NULL, NULL)) == -1) {
      perror("accept error");
      continue;
    }

    while ( (readcount=read(client_fd,buf,sizeof(buf))) > 0) { // 在会话中, 等候client发数据
      printf("read client %u bytes: %.*s", readcount, readcount, buf);
      // echo back
      int wcount=0;

      // 将 echo 值复制 3 次到 buf_mutiline 中
      memset(buf_mutiline,0,500*sizeof(char));
      memcpy(buf_mutiline, buf, readcount);
      memcpy(buf_mutiline+readcount, buf, readcount);
      memcpy(buf_mutiline+readcount*2, buf, readcount);

      //if ((wcount=write(client_fd, buf, readcount)) != readcount) { // echo 单行缓存
      if ((wcount=write(client_fd, buf_mutiline, readcount*3)) != readcount*3) { // echo 3行缓存
          if (readcount > 0) fprintf(stderr,"partial write %d \n", wcount);
          else {
            perror("write error");
            exit(-1);
          }
      }
    }
    if (readcount == -1) {
      perror("read");
      exit(-1);
    }
    else if (readcount == 0) {  // client 会话 close, 重新回到 accept() 等候
      printf("EOF\n");
      close(client_fd);
    }
  }


  return 0;
}