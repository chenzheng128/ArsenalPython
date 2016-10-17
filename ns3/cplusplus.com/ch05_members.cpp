// http://www.cplusplus.com/doc/tutorial/classes2/
// ch05_members.cpp
#include <iostream>
#include <string>
using namespace std;

// classes and default constructors
class Example3 {
    string data; // 存放类
  public:
    Example3 (const string& str) : data(str) {}
    Example3() {}
    const string& content() const {return data;}
};

// destructors
#include <iostream>
#include <string>
using namespace std;

class Example4 {
    string* ptr; // 存放指针
  public:
    // constructors:
    Example4() : ptr(new string) {}  // new
    Example4 (const string& str) : ptr(new string(str)) {}
    // destructor:
    ~Example4 () {delete ptr;}       // delete
    // access content:
    const string& content() const {return *ptr;}
};

// copy constructor: deep copy
#include <iostream>
#include <string>
using namespace std;

class Example5 {
    string* ptr;
  public:
    Example5 (const string& str) : ptr(new string(str)) {}
    ~Example5 () {delete ptr;}
    // copy constructor:
    Example5 (const Example5& x) : ptr(new string(x.content())) {}
    // access content:
    const string& content() const {return *ptr;}
};

// move constructor/assignment
class Example6 {
    string* ptr;
  public:
    Example6 (const string& str) : ptr(new string(str)) {}
    ~Example6 () {delete ptr;}
    // move constructor
    Example6 (Example6&& x) : ptr(x.ptr) {x.ptr=nullptr;}
    // move assignment
    Example6& operator= (Example6&& x) { // TODO 两个&&的含义
      delete ptr;
      ptr = x.ptr;
      x.ptr=nullptr;
      return *this;
    }
    // access content:
    const string& content() const {return *ptr;}
    // addition:
    Example6 operator+(const Example&& rhs) {
      return Example6(content()+rhs.content());
    }
};


int main () {
  Example3 foo;
  Example3 bar ("Example");

  cout << "Examples3 bar's content: " << bar.content() << '\n';

  Example4 foo4;
  Example4 bar4 ("Example");

  cout << "Examples4 (对应  new 的时候要 delete )\n bar4's content: " << bar4.content() << '\n';

  cout << "Examples5 在constructor 中实现 deep copy\n";
  Example5 foo5("Example");
  Example5 bar5 = foo5;
  cout << " bar's content: " << bar5.content() << '\n';

  cout << "Examples6 移动数据\n";
  Example6 foo6 ("Exam");
  Example6 bar6 = Example6("ple");   // move-construction

  foo6 = foo6 + bar6;                  // move-assignment

  cout << " foo's content: " << foo6.content() << '\n';
  return 0;
}