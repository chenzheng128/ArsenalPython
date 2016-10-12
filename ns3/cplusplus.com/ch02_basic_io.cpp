// i/o example
// Source: http://www.cplusplus.com/doc/tutorial/basic_io/

#include <iostream>
using namespace std;

int main ()
{
  int i;
  cout << "Please enter an integer value: ";
  cin >> i;
  cout << "The value you entered is " << i;
  cout << " and its double is " << i*2 << ".\n";
  // return 0;

  string mystring;
  cout << "Please enter an string without whitespace: ";
  cin >> mystring; // cin 不支持空格输入, 会拆分为多个输入
  cout << "mystring =  " << mystring << endl;

  string mystr;
  cout << "What's your name? ";
  getline (cin, mystr); // getline 支持空格 (whitespaces, tabs, new-line...)
  cout << "Hello " << mystr << ".\n";
  cout << "What is your favorite team? ";
  getline (cin, mystr);
  cout << "I like " << mystr << " too!\n";

  //stringstrem 作字符转换
  string mystr2 ("1204");
  int myint;
  // Mac 下编译不过
  //stringstream(mystr2) >> myint;

  return 0;
}