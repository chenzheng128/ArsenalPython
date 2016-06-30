/**
传送引号字符串, 并解析为新参数
Source: http://stackoverflow.com/questions/1706551/parse-string-into-argv-argc

./parse-string-into-argv-argc "i am ok look"
== 4
[i]
[am]
[ok]
[look]
*/

#include <stdio.h>

static int setargs(char *args, char **argv)
{
   int count = 0;

   while (isspace(*args)) ++args;
   while (*args) {
     if (argv) argv[count] = args;
     while (*args && !isspace(*args)) ++args;
     if (argv && *args) *args++ = '\0';
     while (isspace(*args)) ++args;
     count++;
   }
   return count;
}

char **parsedargs(char *args, int *argc)
{
   char **argv = NULL;
   int    argn = 0;

   if (args && *args
    && (args = strdup(args))
    && (argn = setargs(args,NULL))
    && (argv = malloc((argn+1) * sizeof(char *)))) {
      *argv++ = args;
      argn = setargs(args,argv);
   }

   if (args && !argv) free(args);

   *argc = argn;
   return argv;
}

void freeparsedargs(char **argv)
{
  if (argv) {
    free(argv[-1]);
    free(argv-1);
  }
}

int main(int argc, char *argv[])
{
  int i;
  char **argv_new;
  int argc_new;
  char *input_cmd_str = NULL;

  if (argc > 1) input_cmd_str = argv[1];

  argv_new = parsedargs(input_cmd_str,&argc_new);
  printf("== %d\n",argc_new);
  for (i = 0; i < argc_new; i++)
    printf("[%s]\n",argv_new[i]);

  freeparsedargs(argv_new); //释放内存
  exit(0);
}