// implicit conversion of classes:
#include <iostream>
#include <typeinfo>
using namespace std;

class A {};

class B {
public:
  // conversion from A (constructor):
  B (const A& x) {}
  // conversion from A (assignment):
  B& operator= (const A& x) {return *this;}
  // conversion to A (type-cast operator)
  operator A() {return A();}
};

class Dummy {
    double i,j;
  public:
    void set_values(double x, double y) {i=x; j=y;}
};

class Addition {
    int x,y;
  public:
    Addition (int a, int b) { x=a; y=b; }
    int result() { return x+y;}
};

// dynamic_cast
#include <exception>
class Base { virtual void dummy() {} };
class Derived: public Base { int a; };

// const_cast
void print (char * str)
{
  cout << str << '\n';
}

int main ()
{

  cout << "debug: 隐式的类型转换" << endl;
  A foo;
  B bar = foo;    // calls constructor
  bar = foo;      // calls assignment
  foo = bar;      // calls type-cast operator

  cout << "debug: class 类型转换" << endl;
  Dummy d;
  d.set_values(1.0, 2.0);
  Addition * padd;
  padd = (Addition*) &d;
  cout << padd->result() << endl; //TODO 这样转换有何意义呢? 数值并未传递


  cout << "debug: dynamic_cast ..." << endl;
  try {
    Base * pba = new Derived;
    Base * pbb = new Base;
    Derived * pd;

    pd = dynamic_cast<Derived*>(pba);
    if (pd==0) cout << "Null pointer on first type-cast.\n";

    pd = dynamic_cast<Derived*>(pbb);
    if (pd==0) cout << "Null pointer on second type-cast.\n";

    cout << "pd is: " << typeid(pd).name() << '\n';
    cout << "pba is: " << typeid(pba).name() << '\n';
    cout << "pbb is: " << typeid(pbb).name() << '\n';

  } catch (exception& e) {cout << "Exception: " << e.what();}

  cout << "debug: const_cast 将 const 参数转为非 const ..." << endl;
  const char * c = "sample text";
  print ( const_cast<char *> (c) );


  cout << "debug: #include <typeinfo> 使用typeid判断类型";
  int * a,b;
  a=0; b=0;
  if (typeid(a) != typeid(b)) //  类似 typeof()
  {
    cout << "a and b are of different types:\n";
    cout << "a is: " << typeid(a).name() << '\n';
    cout << "b is: " << typeid(b).name() << '\n';
  }

  return 0;
}