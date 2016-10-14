// strings and NTCS:
// http://www.cplusplus.com/doc/tutorial/ntcs/
#include <iostream>
#include <string>
using namespace std;

int main ()
{

  cout << "c-string 和 string 类的互转" << endl;
  char myntcs[] = "some text"; //c-string
  string mystring = myntcs;  // convert c-string to string
  cout << mystring << endl;          // printed as a library string
  cout << mystring.c_str() << endl ;  // printed as a c-string


  cout << "c-string 固定长度, 而string 动态长度" << endl;
  char question1[] = "What is your name? ";
  string question2 = "Where do you live? ";
  char answer1 [80];
  string answer2;
  cout << question1;
  cin >> answer1;
  cout << question2;
  cin >> answer2;
  cout << "Hello, " << answer1;
  cout << " from " << answer2 << "!\n";


  return 0;
}