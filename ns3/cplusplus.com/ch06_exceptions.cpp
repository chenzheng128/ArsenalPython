// exceptions
// http://www.cplusplus.com/doc/tutorial/exceptions/

#include <iostream>
using namespace std;

// 3种函数定义
// 指定类型
double myfunction1 (char param) throw (int); // 抛出 int 时 调用 std::terminate.
// 不指定类型
int myfunction2 (int param) throw(); // 调用 std::unexpected , all exceptions call unexpected
// 无 throw 定义
int myfunction3 (int param);         // 不调用 std::unexpected , normal exception handling


// 自定义异常类
class myexception: public exception
{
  public:
  virtual const char* what() const throw()
  {
    return "My exception happened";
  }
} myex;


int main () {
  try
  {
      try { // 嵌套 exception
      // throw code here
      }
      catch (int n) {
          throw;
      }

    throw 20;
  }
  catch (int e)
  {
    cout << "An int exception occurred. Exception Nr. " << e << '\n';
  }
  catch (char param) { cout << "char exception"; }
  catch (...) { cout << "default exception"; } // default 异常
  cout << endl;

  cout << "== 自定义异常" << endl;
  try
  {
    exception default_e;
    cout << "debug: deault exception.what() string: " << default_e.what() << '\n';

    throw myex;
  }
  // 不加 & 输出的是 std::exception, why?
  // 因为不加 & 时, 进行的是复制, 而由复制初始化出exception的what()默认返回的就是std::exception.
  // 不加 & 时, 如改为 (myexception& e) 输出就正确了
  catch (exception& e)
  {
    cout << e.what() << '\n';
  }

  cout << "== 常用异常: 检查 内存申请" << endl;
  /*
  常见 exception
bad_alloc	thrown by new on allocation failure
bad_cast	thrown by dynamic_cast when it fails in a dynamic cast
bad_exception	thrown by certain dynamic exception specifiers
bad_typeid	thrown by typeid
bad_function_call	thrown by empty function objects
bad_weak_ptr	thrown by shared_ptr when passed a bad weak_ptr

logic_error	error related to the internal logic of the program
runtime_error	error detected during runtime
  */
  try
  {
    int* myarray= new int[1000];
  }
  catch (exception& e)
  {
    cout << "Standard exception: " << e.what() << endl;
  }

  return 0;
}