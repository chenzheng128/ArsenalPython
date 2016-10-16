// ch05_inheritance.cpp
// http://www.cplusplus.com/doc/tutorial/inheritance/

// derived classes
#include <iostream>
using namespace std;

class Polygon {
  protected:
    int width, height;
  public:
    void set_values (int a, int b)
      { width=a; height=b;}
 };

class Rectangle: public Polygon { // 从Polygon 继承
  public:
    int area ()
      { return width * height; }
 };

class Triangle: public Polygon { // 从Polygon 继承
  public:
    int area ()
      { return width * height / 2; }
  };

// constructor 的继承关系
class Mother {
  public:
    Mother ()
      { cout << "Mother: no parameters\n"; }
    Mother (int a)
      { cout << "Mother: int parameter\n"; }
};

class Daughter : public Mother {
  public:
    Daughter (int a)  // 父类使用默认无参的constructor
      { cout << "Daughter: int parameter\n\n"; }
};

// derived_constructor_name (parameters) : base_constructor_name (parameters) {...}
class Son : public Mother {
  public:
    Son (int a) : Mother (a)  // 父类使用int参数的constructor
      { cout << "Son: int parameter\n\n"; }
};


int main () {
  cout << "== 分别计算 Polygon 两个子类 Rectangle/Triangle 的面积大小\n";
  Rectangle rect;
  Triangle trgl;
  rect.set_values (4,5);
  trgl.set_values (4,5);
  cout << "Rectangle: " << rect.area() << '\n';
  cout << "Triangle: " << trgl.area() << '\n';

  /* 类的访问范围
  Access	public	protected	private
  members of the same class	yes	yes	yes
  members of derived class	yes	yes	no
  not members	yes	no	no
  */

  cout << "== constructor 的继承关系" << endl;
  cout << "// 父类使用默认无参的constructor\n";
  Daughter kelly(0);
  cout << "// 父类使用int参数的constructor\n";
  Son bud(0);

  cout << "== 多重继承的例子( 用cpp.sh )";
  // 比较简单在 http://cpp.sh/23k 运行即可 (可能不被保存)

  return 0;
}