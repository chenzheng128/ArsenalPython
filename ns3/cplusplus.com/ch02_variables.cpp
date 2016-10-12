/**
// initialization of variables
Source: http://www.cplusplus.com/doc/tutorial/variables/
*/

#include <iostream>
#include <string>
using namespace std;

int main ()
{
  int a=5;               // initial value: 5
  int b(3);              // initial value: 3
  // int c{2};              // initial value: 2  // Mac OSX 不支持
  int c(2);
  int result;            // initial value undetermined

  int foo = 0;
  auto bar1 = foo;  // the same as: int bar = foo;
  bar1 = 1;
  decltype(foo) bar2;  // the same as: int bar;
  bar2 = 2;
  cout << "auto decltype: "<< bar1 << " " << bar2 << endl;

  a = a + b;
  result = a - c;
  cout << result << "\n";


  string mystring;
  mystring = "This is a string";
  cout << mystring << "\n";

  // endl 结束行并 flush;  endl manipulator ends the line (printing a newline character and flushing the stream).
  mystring = "This is the initial string content";
  cout << mystring << endl;
  mystring = "This is a different string content";
  cout << mystring << endl;
  return 0;
  return 0;
}