// function macro
// http://www.cplusplus.com/doc/tutorial/preprocessor/

#include <iostream>
using namespace std;

#define getmax(a,b) ((a)>(b)?(a):(b))

int main()
{
  int x=5, y;
  y= getmax(x,2);
  cout << y << endl;
  cout << getmax(7,x) << endl;

  cout << "== 宏定义 define/undefine" << endl;
  #define TABLE_SIZE 100
  int table1[TABLE_SIZE];
  #undef TABLE_SIZE
  #define TABLE_SIZE 200
  int table2[TABLE_SIZE];

  cout << "== 宏定义 # : 相当于cout << test" << endl;
  #define str(x) #x  // '#' 代表引用变量x, 类似于 $x
  cout << str(test) << endl;

  cout << "== 宏定义 ## cout : 相当于cout << test" << endl;
  #define glue(a,b) a ## b // '##' 代表两个变量之间无空格
  glue(c,out) << "test" << endl;

  cout << "== 宏定义 if else endif defined" << endl;
  #if TABLE_SIZE>200
    #undef TABLE_SIZE
    #define TABLE_SIZE 200
  #elif TABLE_SIZE<50
    #undef TABLE_SIZE
    #define TABLE_SIZE 50
  #else
    #undef TABLE_SIZE
    #define TABLE_SIZE 100
  #endif

  #if defined ARRAY_SIZE
    #define TABLE_SIZE2 ARRAY_SIZE
  #elif !defined BUFFER_SIZE
    #define TABLE_SIZE2 128
  #else
    #define TABLE_SIZE2 BUFFER_SIZE
  #endif

  cout << "== 预处理 #error 编译前检查, 需要c++编译器\n";
  #ifndef __cplusplus
  #error A C++ compiler is required!
  #endif

  cout << "== 预处理 #include <header> #include file\n";



  cout << "== 预处理 #line_number filename\n";
  cout << " 修改 行号 与 文件名 \n";
  cout << " 这里定义完line_number后, 会修改整个文件当前行 __LINE__ 宏\n";
  cout << " 这里定义完filename后, 会修改文件名 __FILE__ 宏\n";
  // #line 20 "myfile.cpp:"
  // int a?;

  cout << "== 预处理 预定义宏名称 Predefined macro names\n";

  cout << "This is the line number " << __LINE__;
  cout << " of file " << __FILE__ << ".\n";
  cout << "Its compilation began " << __DATE__;
  cout << " at " << __TIME__ << ".\n";
  cout << "The compiler gives a __cplusplus value of " << __cplusplus;
  return 0;
}
