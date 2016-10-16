// friend functions
#include <iostream>
using namespace std;

class Square;

class Rectangle {
    int width, height;
  public:
    Rectangle() {}
    Rectangle (int x, int y) : width(x), height(y) {}
    int area() {return width * height;}
    friend Rectangle duplicate (const Rectangle&); // friend func
    void convert (Square a);
};

// friend func
Rectangle duplicate (const Rectangle& param)
{
  Rectangle res;
  res.width = param.width*2;
  res.height = param.height*2;
  return res;
}

// friend class
class Square {
  friend class Rectangle; // Rectangle 变成我的好朋友
  private:
    int side;
  public:
    Square (int a) : side(a) {}
};

void Rectangle::convert (Square a) {
  width = a.side;    // 不是好朋友就玩不了这一套
  height = a.side;
}

int main () {
  Rectangle foo;
  Rectangle bar (2,3);

  cout << "== friend 函数:\n duplicate 变成了" \
    "Rectangle 的朋友方法, 虽然它不在 Rectangle:: 命名空间下, " \
    "但是它可以访问private 变量 .width .height\n";
  foo = duplicate (bar);
  cout << foo.area() << '\n';

  cout << "== friend 类:\n Square 变成了" \
    "Rectangle 的好朋友, 家里的 .side 都向你打开\n";
  Rectangle rect;
  Square sqr (4);
  rect.convert(sqr);
  cout << rect.area();
  return 0;
}