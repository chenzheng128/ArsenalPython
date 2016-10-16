// virtual members
#include <iostream>
using namespace std;

class Polygon {
  protected:
    int width, height;
  public:
    void set_values (int a, int b)
      { width=a; height=b; }

    // abstract 抽象类定义, 不能初始化 base类
    // virtual int area () =0;

    // virtual 函数定义, 可以初始化 base类
    // 文档中提到Non-virtual members can also be redefined in derived classes
    // 非 virtual member 也可以被继承, 但是不能通过 base 类来进行访问 继承方法
    // 如果去掉 area() 之前的结果, 如下的输出结果会变成  0, 0 ,0
    virtual int area () { return 0; }
};

class Rectangle: public Polygon {
  public:
    int area ()
      { return width * height; }
};

class Triangle: public Polygon {
  public:
    int area ()
      { return (width * height / 2); }
};

int main () {

  cout << "== virtual 类" \
  " 如果去掉 area() 之前的结果, 如下的输出结果会变成  0, 0 ,0 \n";
  Rectangle rect;
  Triangle trgl;
  Polygon poly;
  Polygon * ppoly1 = &rect;
  Polygon * ppoly2 = &trgl;
  Polygon * ppoly3 = &poly;
  ppoly1->set_values (4,5);
  ppoly2->set_values (4,5);
  ppoly3->set_values (4,5);
  cout << ppoly1->area() << '\n';
  cout << ppoly2->area() << '\n';
  cout << ppoly3->area() << '\n';
  return 0;
}