// classes example
// http://www.cplusplus.com/doc/tutorial/classes/

#include <iostream>
using namespace std;

class Rectangle {
    int width, height;
  public:
    Rectangle ();        // Constructors
    Rectangle (int,int); // Constructors
    void set_values (int,int);
    int area() {return width*height;}
};

// scope operator (::, two colons),
void Rectangle::set_values (int x, int y) {
  width = x;
  height = y;
}

// Constructors
Rectangle::Rectangle () {
  width = 5;
  height = 5;
}

Rectangle::Rectangle (int a, int b) {
  width = a;
  height = b;
}

class Circle {
    double radius;
  public:
    Circle(double r) { radius = r; }
    double circum() {return 2*radius*3.14159265;}
};


int main () {
  // Rectangle rect;
  Rectangle rect(1, 1);
  rect.set_values (3,4);
  cout << "area: " << rect.area() << endl;

  cout << "debug: 不同的 constructure 方法 "<< endl;
  Circle foo (10.0);   // functional form
  Circle bar = 20.0;   // assignment init.
  // Mac 编译不过
  // Circle baz {30.0};   // uniform init.
  // Circle qux = {40.0}; // POD-like

  cout << "foo's circumference: " << foo.circum() << '\n';

  cout << "debug: 指向对象的指针 ";
  Rectangle * foo2, * bar2, * baz;
  foo2 = &rect;
  bar2 = new Rectangle (5, 6);
  // Mac 下编译不过, 改用 set_values 的初始方式
  // baz = new Rectangle[2] { {2,5}, {3,6} };
  baz = new Rectangle[2] ; // 数组指针
  baz[0].set_values(2, 5);
  baz[1].set_values(3, 6);
  cout << "obj's area: " << rect.area() << '\n';
  cout << "*foo's area: " << foo2->area() << '\n';
  cout << "*bar's area: " << bar2->area() << '\n';
  cout << "baz[0]'s area:" << baz[0].area() << '\n';
  cout << "baz[1]'s area:" << baz[1].area() << '\n';
  delete bar2;
  delete[] baz;
  return 0;
}