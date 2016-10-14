// rememb-o-matic
// Source: http://www.cplusplus.com/doc/tutorial/dynamic/
/**
原有 c 的 malloc 函数还是可以用的, 但是和  new 与 delete 不是一个体系, 两个体系不能混用
C++ integrates the operators new and delete for allocating dynamic memory. But these were not available in the C language; instead, it used a library solution, with the functions malloc, calloc, realloc and free, defined in the header <cstdlib> (known as <stdlib.h> in C). The functions are also available in C++ and can also be used to allocate and deallocate dynamic memory.
*/

#include <iostream>
#include <new>
using namespace std;

int main ()
{
  int i,n;
  int * p;
  cout << "How many numbers would you like to type? ";
  cin >> i;
  cout <<  "debug: 动态创建" <<  i << "个元素大小的int[i]数组" << endl;

  // 新建数组;  nothrow 可以避免异常 (Error: memory could not be allocated).
  p= new (nothrow) int[i];


  if (p == nullptr)
    cout << "Error: memory could not be allocated";
  else
  {
    for (n=0; n<i; n++)
    {
      cout << "Enter number: ";
      cin >> p[n];
    }
    cout << "You have entered: ";
    for (n=0; n<i; n++)
      cout << p[n] << ", ";
    cout << endl;

    cout <<  "debug: 删除" <<  i << "个元素大小的int[i]数组" << endl;
    delete[] p;
  }
  return 0;
}