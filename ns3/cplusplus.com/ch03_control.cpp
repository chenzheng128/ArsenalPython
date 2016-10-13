// custom countdown using while
// http://www.cplusplus.com/doc/tutorial/control/
#include <iostream>
using namespace std;

int main ()
{

  // while loop
  int n = 10;

  while (n>0) {
    cout << n << ", ";
    --n;
  }

  cout << "while loop liftoff!\n";

  // for loop
  for (int n=10; n>0; n--) {
    cout << n << ", ";
  }
  cout << "for loop liftoff!\n";

  // 双变量的 for loop 例子
  for ( int n2=0, i=10 ; n2!=i ; ++n2, --i )
  {
    // whatever here...
    cout << n2 << ", ";
  }
  cout << "for loop (双变量) liftoff!\n";

  // warning: auto / range-based for loop is a C++11 extension [-Wc++11-extensions]
  string str2 ("Hello!");
  for (char c : str2) {
    cout << "[" << c << "]";
  }
  cout << " 循环 for ( declaration : range ) statement; 例子 \n";

  for (auto c : str2) {
    cout << "[" << c << "]";
  }
  cout << " 使用 auto 改进 \n";


  // break; continue; 跳过
  n=10;
mylabel:
  cout << n << ", ";
  n--;
  if (n>0) goto mylabel;
  cout << "goto mylable: liftoff!\n";

  // do while loop
  string str;
  do {
    cout << "Enter text: ";
    getline (cin,str);

    switch (stoi( str )) { // 字符串转换 std::stoi
      case 1:
      case 2:
      case 3:
        cout << "x is 1, 2 or 3\n";
        break;
      default:
        cout << "You entered: " << str << '\n';
    }

  } while (str != "goodbye");

}