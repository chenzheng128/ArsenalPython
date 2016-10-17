// default and delete implicit members
// http://www.cplusplus.com/doc/tutorial/classes2/

#include <iostream>
using namespace std;

class Rectangle {
    int width, height;
  public:
    Rectangle (int x, int y) : width(x), height(y) {}
    Rectangle() = default;  // default
    Rectangle (const Rectangle& other) = delete; //delete 之后就不能使用了

    // 下面这两句的效果是一样的
    // Rectangle::Rectangle (const Rectangle& other) = default;
    // Rectangle::Rectangle (const Rectangle& other) : width(other.width), height(other.height) {}

    int area() {return width*height;}
};

int main () {
  Rectangle foo;
  Rectangle bar (10,20);

  // Rectangle foo2(bar); //delete 之后就不能使用了

  cout << "bar's area: " << bar.area() << '\n';
  return 0;
}