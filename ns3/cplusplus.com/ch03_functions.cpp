// ch03_functions.cpp
// http://www.cplusplus.com/doc/tutorial/functions/

// function example
#include <iostream>
using namespace std;

int addition(int a, int b); //对函数的预先定义

int addition (int a, int b)
{
  int r;
  r=a+b;
  return r;
}

int subtraction (int a, int b)
{
  int r;
  r=a-b;
  return r;
}

void printmessage ()
{
  cout << "I'm a void() function!" << endl;
}

// reference access
void duplicate_reference (int& a, int& b, int& c)
{
  a*=2;
  b*=2;
  c*=2;
}

// 更经济的传递 string 方式
string concatenate (string& a, string& b)
{
  return a+b;
}

// 不仅经济, 而且保护了该变量
string concatenate (const string& a, const string& b)
{
  return a+b;
}

int divide (int a, int b=2)
{
  int r;
  r=a/b;
  return (r);
}

int main ()
{
  int z;
  z = addition (5,3);
  cout << "The addition() result is " << z << endl;

  int x=5, y=3;
  z = subtraction (7,2);
  cout << "The first result z is " << z << '\n';
  cout << "The second subtraction () result is " << subtraction (7,2) << '\n';
  cout << "The third subtraction () result is " << subtraction (x,y) << '\n';
  z= 4 + subtraction (x,y);
  cout << "The fourth subtraction () result is " << z << '\n';

  printmessage ();


  cout << "x , y origned value: " << x << " " << y << endl;
  duplicate_reference(x, y, x);
  cout << "x , y has been duplicated: " << x << " " << y << endl;


}