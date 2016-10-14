// arrays example
// http://www.cplusplus.com/doc/tutorial/arrays/

#include <iostream>
#include <array>
using namespace std;

#define WIDTH 5
#define HEIGHT 3

int foo [] = {16, 2, 77, 40, 12071};
int i, result=0;

void printarray (int arg[], int length) {
  for (int n=0; n<length; ++n)
    cout << arg[n] << ' ';
  cout << '\n';
}

int main ()
{
  for ( i=0 ; i<5 ; ++i )
  {
    result += foo[i];
  }
  cout << result << endl;


  // 二维数据

  int jimmy [HEIGHT][WIDTH];
  int n,m;

  for (n=0; n<HEIGHT; n++)
    for (m=0; m<WIDTH; m++)
    {
      jimmy[n][m]=(n+1)*(m+1);
    }

  cout << "数组作为函数参数参数" << endl;
  int firstarray[] = {5, 10, 15};
  int secondarray[] = {2, 4, 6, 8, 10};
  printarray (firstarray,3);
  printarray (secondarray,5);


  cout << "<array.h> 模板 container " << endl;

  array<int,3> myarray  = {10,20,30};

  for (int i=0; i<myarray.size(); ++i)
    ++myarray[i];

  for (int elem : myarray)
    cout << elem << '\n';

  return 0;
}