// overloading functions
// http://www.cplusplus.com/doc/tutorial/functions2/

#include <iostream>
using namespace std;

// 自动依据参数选择函数 overload
int operate (int a, int b)
{
  return (a*b);
}

double operate (double a, double b)
{
  return (a/b);
}

// function template
#include <iostream>
using namespace std;

template <class T>
T sum (T a, T b)
{
  T result;
  result = a + b;
  return result;
}

template <class T, class U>
bool are_equal (T a, U b)
{
  return (a==b);
}


template <class T, int N>
T fixed_multiply (T val)
{
  return val * N;
}

int main ()
{
  //overload
  int x=5,y=2;
  double n=5.0,m=2.0;
  cout << operate (x,y) << '\n';
  cout << operate (n,m) << '\n';

  //template
  int i=5, j=6, k;
  double f=2.0, g=0.5, h;
  k=sum<int>(i,j);
  h=sum<double>(f,g);
  cout << k << '\n';
  cout << h << '\n';

  if (are_equal(10,10.0))  // 相当于 are_equal<int,double>(10,10.0)
    cout << "x and y are equal\n";
  else
    cout << "x and y are not equal\n";

  // Non-type template arguments // 函数阶段编译进去 2 / 3
  cout << fixed_multiply<int,2>(10) << '\n';
  cout << fixed_multiply<int,3>(10) << '\n';
  return 0;
}