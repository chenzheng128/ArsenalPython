// namespaces
// http://www.cplusplus.com/doc/tutorial/namespaces/

#include <iostream>
using namespace std;

namespace foo
{
  int value() { return 5; }
}

namespace bar
{
  const double pi = 3.1416;
  double value() { return 2*pi; }
}

namespace first
{
  int x = 5;
  int y = 10;
}

namespace second
{
  double x = 3.1416;
  double y = 2.7183;
}

int var_global;

int main () {
  cout << foo::value() << '\n';
  cout << bar::value() << '\n';
  cout << bar::pi << '\n';

  // using 有点像 import
  using first::x;
  using second::y;
  cout << x << '\n';
  cout << y << '\n';
  cout << first::y << '\n';
  cout << second::x << '\n';

  using namespace first;
  cout << x << '\n';
  cout << y << '\n';

  cout << "using 仅在一个 block 中生效" << endl;
  {
    using namespace first;
    cout << x << '\n';
  }
  {
    using namespace second;
    cout << x << '\n';
  }

  int var_local; //教程例子中local变量不会自动初始化, 但是我们这里也初始化为 0 了
  cout << "检查变量初始化: " << endl ;
  cout << var_global << endl;
  cout << var_local << endl;
  return 0;
}