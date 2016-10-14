// my first pointer
// http://www.cplusplus.com/doc/tutorial/pointers/
#include <iostream>
using namespace std;


// void 指针
void increase (void* data, int psize)
{
  if ( psize == sizeof(char) )
  { char* pchar; pchar=(char*)data; ++(*pchar); }
  else if (psize == sizeof(int) )
  { int* pint; pint=(int*)data; ++(*pint); }
}


// 函数指针

int addition (int a, int b)
{ return (a+b); }

int subtraction (int a, int b)
{ return (a-b); }

int operation (int x, int y, int (*functocall)(int,int))
{
  int g;
  g = (*functocall)(x,y);
  return (g);
}


int main ()
{
  int firstvalue, secondvalue;
  int * mypointer;

  mypointer = &firstvalue;
  *mypointer = 10;
  mypointer = &secondvalue;
  *mypointer = 20;
  cout << "firstvalue is " << firstvalue << '\n';
  cout << "secondvalue is " << secondvalue << '\n';

  firstvalue = 5, secondvalue = 15;
  int * p1, * p2;

  p1 = &firstvalue;  // p1 = address of firstvalue
  p2 = &secondvalue; // p2 = address of secondvalue
  *p1 = 10;          // value pointed to by p1 = 10
  *p2 = *p1;         // value pointed to by p2 = value pointed to by p1
  p1 = p2;           // p1 = p2 (value of pointer is copied)
  *p1 = 20;          // value pointed to by p1 = 20

  cout << "firstvalue is " << firstvalue << '\n';
  cout << "secondvalue is " << secondvalue << '\n';


  cout << "指针与数组" << endl;
  int numbers[5];
  int * p;
  p = numbers;  *p = 10;
  p++;  *p = 20;
  p = &numbers[2];  *p = 30;
  p = numbers + 3;  *p = 40;
  p = numbers;  *(p+4) = 50;
  for (int n=0; n<5; n++)
    cout << numbers[n] << ", ";
  cout << endl;

  cout << "指向指针的指针" << endl;
  char a;
  char * b;
  char ** c;
  a = 'z';
  b = &a;
  c = &b;


  cout << "void* 指针 (使用时确认大小) " << endl;
  char a1 = 'x';
  int b1 = 1602;
  increase (&a1,sizeof(a1));
  increase (&b1,sizeof(b1));
  cout << a1 << ", " << b1 << '\n';

  cout << "空指针" << endl;
  int * p_null = 0;
  int * q_null = nullptr;
  q_null = NULL;

  cout << "函数指针" << endl;
  int m,n;
  int (*minus)(int,int) = subtraction;

  m = operation (7, 5, addition);
  n = operation (20, m, minus);
  cout << m << " " << n << endl;

  return 0;
}