#include <string>

// http://ysonggit.github.io/coding/2015/01/01/variable-length-array-for-non-pod-element-type.html
// pod_array.cc:10:8: error: variable length array of non-POD element type 'Foo'

struct Foo{
    std::string val;
};


int main(){
  int n = 5;

// not working in MacOSX clang
//  Foo a[n];
//  const size_t m =10;
//  Foo b[m];

  Foo *a = new Foo[n];
  delete [] a;
  a = NULL; // clear to prevent using invalid memory reference (dangling pointer)
}