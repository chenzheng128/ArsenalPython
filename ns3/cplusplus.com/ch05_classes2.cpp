// overloading operators example
#include <iostream>
using namespace std;

class CVector {
  public:
    int x,y;
    CVector () {};
    CVector (int a,int b) : x(a), y(b) {}
    // CVector operator + (const CVector&);
    CVector operator - (const CVector&);
    CVector& operator = (const CVector&);
};

// 作为 member 的重载
CVector CVector::operator- (const CVector& param) {
  CVector temp;
  temp.x = x + param.x;
  temp.y = y + param.y;
  return temp;
}

CVector& CVector::operator= (const CVector& param)
{
  x=param.x;
  y=param.y;
  return *this;
}

// 作为non-member 的重载. 效果是一样的
CVector operator+ (const CVector& lhs, const CVector& rhs) {
  CVector temp;
  temp.x = lhs.x + rhs.x;
  temp.y = lhs.y + rhs.y;
  return temp;
}

// this 关键词使用
class Dummy {
  public:
    static int n; // 静态变量
    Dummy () { n++; };
    bool isitme (Dummy& param);
};

int Dummy::n=0;

bool Dummy::isitme (Dummy& param)
{
  if (&param == this) return true;
  else return false;
}

// const 也能被重载 可怕的c++
class MyClass {
    int x;
  public:
    MyClass(int val) : x(val) {}

    // 返回不可修改的 x
    const int& get() const {return x;}

    // 返回可修改的 x ; TODO 为什么这里不用 &x 呢?
    // 这个 get 是可以如下被当做 set() 来使用的
    // expression is assignable
    // foo2.get() = 15;
    int& get() {return x;}

    int get_x() {return x;} // 返回 x 值
};

int main () {
  CVector foo (3,1);
  CVector bar (1,2);
  CVector result, result2;
  result = foo - bar;
  result2 = foo + bar;
  cout << "\n// 作为 member 的重载" << endl;
  cout << result.x << ',' << result.y << '\n';
  cout << "// 作为non-member 的重载. 效果是一样的" << endl;
  cout << result2.x << ',' << result2.y << '\n';

  cout << "\n// this 关键词使用 " << endl;
  Dummy a1;
  Dummy* b1 = &a1;

  if ( b1->isitme(a1) )
    cout << "yes, &a1 is b1\n";

  cout << "\n// static 变量 n 累加 " << endl;
  Dummy b[5];
  cout << a1.n << '\n';
  Dummy * c = new Dummy;
  cout << Dummy::n << '\n';
  delete c;

  cout << "\n// 声明 const 只读类 " << endl;
  const CVector vec_readonly(10, 10);
  // vec_readonly.x = 5            // // not valid: x cannot be modified
  cout << vec_readonly.x << '\n';  // ok: data member x can be read

  cout << "\n// const 也能被重载 可怕的c++" << endl;
  MyClass foo2 (10);
  const MyClass bar2 (20);
  foo2.get() = 15;         // ok: get() returns int&
  // bar.get() = 25;        // not valid: get() returns const int&
  cout << foo2.get() << '\n';
  cout << bar2.get() << '\n';

  return 0;
}