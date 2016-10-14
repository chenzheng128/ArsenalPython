// http://www.cplusplus.com/doc/tutorial/other_data_types/

#include <iostream>
using namespace std;

// type aliais
// 定义
typedef char C;
typedef unsigned int WORD;
typedef char * pChar;
typedef char field [50];

// 声明
C mychar, anotherchar, *ptc1;
WORD myword;
pChar ptc2;
field name;

// union 一个内存区, 用不同位置进行访问
union mytypes_t {
  char c;
  int i;
  float f;
} mytypes;

// 包含 数据结构的 union
union mix_t {
  int l;
  struct {
    short hi;
    short lo;
    } s;
  char c[4];
} mix;

// 匿名 union
struct book2_t {
  char title[50];
  char author[50];
  union {
    float dollars;
    int yen;
  };
} book2;

// 从 0 开始定义 enum
enum colors_t {black, blue, green, cyan, red, purple, yellow, white};

// 从 1 开始定义 enum
enum months_t { january=1, february, march, april,
                may, june, july, august,
                september, october, november, december} y2k;

// enum 类, 而不是 后台是 int 类型
enum class Colors {black, blue, green, cyan, red, purple, yellow, white};

// enum 类, 指定后台为 char
// Mac 下未编译通过
// enum class EyeColor : char {blue, green, brown};

int main() {
  cout << "使用 enum(int) " << endl;
  colors_t mycolor;
  months_t mymonth;
  mymonth = january;
  mycolor = black;
  if (mycolor == green) mycolor = red;
  cout << "enum color: black = "<< mycolor << endl;
  cout << "enum month: january = "<< mymonth << endl;

  cout << "使用 enum(class) " << endl;
  Colors mycolor_cla;
  mycolor_cla = Colors::blue;
  if (mycolor_cla == Colors::green) mycolor_cla = Colors::red;
  // cout << "enum color: blue = "<< Colors::blue << endl;

}